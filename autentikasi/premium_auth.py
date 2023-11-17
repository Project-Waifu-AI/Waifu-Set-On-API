from fastapi import APIRouter, Header
from database.model import premium

app = APIRouter(prefix='/premium', tags=['premium'])

@router.post('/daftar-premium')
async def daftarPremium(access_token: str = Header(...)):
    check = check_access_token_expired(access_token=access_token)
    
    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=401)
    elif check is False:
        payloadJWT = decode_access_token(access_token=access_token)
        user_id = payloadJWT.get('sub')

