from fastapi import APIRouter, HTTPException, Request, Header
from fastapi.responses import RedirectResponse, JSONResponse
from requests_oauthlib import OAuth1Session
from configs import config
import requests
import json

router = APIRouter(prefix='/twiter-auth', tags=['twiter autentikasi0.2 api v.2'])

# set
request_token_url = "https://api.twitter.com/oauth/request_token"
base_authorization_url = "https://api.twitter.com/oauth/authorize"
access_token_url = "https://api.twitter.com/oauth/access_token"
consumer_key = config.consumer_key_twiter
consumer_secret = config.consumer_secret_twiter
fields = "created_at,description"
params = {"user.fields": fields}


@router.get('/autentikasi')
async def login_twiter():
    global fetch_response
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        raise HTTPException(detail="There may have been an issue with the consumer_key or consumer_secret you entered.", status_code=500)
    authorization_url = oauth.authorization_url(base_authorization_url)
    return RedirectResponse(authorization_url)
    
@router.get('/callback-autentikasi')
async def callbackLogin(request: Request):
    pin = request.query_params.get('oauth_verifier')
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=fetch_response.get("oauth_token"),
        resource_owner_secret=fetch_response.get("oauth_token_secret"),
        verifier=pin,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    response = oauth.get("https://api.twitter.com/2/users/me", params=params)

    if response.status_code != 200:
        raise HTTPException(detail=f'status code:{str(response.status_code())}, detail:{response.text()}')

    json_response = response.json()
    return JSONResponse(content=json_response)