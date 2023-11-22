from fastapi import APIRouter, HTTPException, Request, Header
from fastapi.responses import RedirectResponse, JSONResponse
from requests_oauthlib import OAuth2Session
from configs import config
import os
import base64
import hashlib
import os
import re
import requests

router = APIRouter(prefix='/twiter-auth', tags=['twiter autentikasi0.2 api v.2'])

# set
scopes = ["offline.access", "tweet.read", "users.read", "tweet.write"]
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"
user_info_url = "https://api.twitter.com/2/tweets"
code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)
code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

def make_token():
    return OAuth2Session(config.client_id_twiter, redirect_uri=config.redirect_uri_login_twiter, scope=scopes)

@router.get('/login')
async def login():
    global twiter 
    twiter = make_token()
    authorization_url = twiter.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
    )

    return RedirectResponse(url=authorization_url[0])

@router.get('/callback-login')
async def callback_login(code):
    access_token = twiter.fetch_token(
        token_url=token_url,
        client_secret=config.client_secret_twiter,
        code_verifier=code_verifier,
        code=code,
    )
    
    return JSONResponse(content=access_token)

@router.get('/root')
async def root(request:Request):
    access_token = request.query_params.get('access_token')
    r = requests.request(
        "POST",
        "https://api.twitter.com/2/users/:id",
        headers={
            "Authorization": "Bearer {}".format(access_token),
            "Content-Type": "application/json",
        },
    )
    return JSONResponse(content=r.json())

@router.post("/search-user")
async def search_user(
    username: str,
    access_token: str = Header(..., description="twitter access token"),
):
    r = requests.request(
        "GET",
        "https://api.twitter.com/2/users/by/username/{}".format(
            username
        ),
        headers={
            "Authorization": "Bearer {}".format(access_token),
            "Content-Type": "application/json",
        },
    )
    return JSONResponse(content=r.json())
