from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
import secrets
from model import userdata
from webhook.send_email import send
from helping.auth_helper import (
    chek_password
)
from database.model import userdata, access_token_data
from configs import config
from helping import auth_helper

router = APIRouter(prefix='/wso-auth', tags=['Waifu-Set-On-autentikasi'])

@router.get('/login/{email}')
async def login_wso(email: str, password: str):
    user = await userdata.filter(email=email).first()

    if user:
        if user.akunwso is False:
            return RedirectResponse(config.redirect_uri_page_masuk)
        else:
            if not check_password