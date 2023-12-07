from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from body_request.auth_body_request import smd_login, smd_register
from database.model import userdata
from helper.access_token import create_access_token
from helper.cek_and_set import cek_namaku_ada, set_name_unik, cek_admin
from helper.response import auth_response
from configs import config
import requests

router = APIRouter(prefix='/auth/smd', tags=['SMD AUTH'])

@router.post('/login')
async def authLogin(meta: smd_login):
    endpoint = 'auth/login'
    url = f'{config.smd_domain}{endpoint}'
    body = {
        'username': meta.username,
        'password': meta.password
    }
    
    post = requests.post(url=url, json=body)
    if post.status_code != 200:
        raise HTTPException(detail=str(post.text), status_code=post.status_code)
    data = post.json()
    print(data)
    id_smd = data.get('_id')
    nama = data.get('username')
    email = data.get('email')
    
    user = await userdata.filter(email=email).first()
    
    global namaYangDisimpan
    if await cek_namaku_ada(nama=nama) == False:
        namaYangDisimpan = await set_name_unik(nama=nama)
    else:
        namaYangDisimpan = nama
    
    if user:
        
        if user.smdAuth is False:
            
            user.smdAuth = True
            
            if cek_admin is True:
                user.admin = True
                user.AtsumaruKanjo += 999999999
                user.NegaiGoto += 999999999
            else:
                user.AtsumaruKanjo += 100

            if user.nama is None:
                user.nama = namaYangDisimpan
            
            if user.smdID is None:
                user.smdID = id_smd
            
            await user.save()
        
        token = create_access_token(user=user)
        response = auth_response(user=user, token=token)
        return JSONResponse(content=response, status_code=200)
    
    else:
        
        if cek_admin(email=email) is False:
            save = userdata(nama=namaYangDisimpan, email=email, smdAuth=True, AtsumaruKanjo=100, smdID=id_smd)
        else:
            save = userdata(nama=namaYangDisimpan, email=email, smdAuth=True, AtsumaruKanjo = 999999999, NegaiGoto = 999999999, smdID=id_smd, admin=True)
        
        await save.save()
        
        user = await userdata.filter(email=email).first()
        
        token = create_access_token(user=user)
        
        response = auth_response(user=user, token=token)
        return JSONResponse(content=response, status_code=200)
    
@router.post('/register')
async def authRegister(meta: smd_register):
    endpoint = 'auth/login'
    url = f'{config.smd_domain}{endpoint}'
    body = {
        'username': meta.username,
        'email': meta.email,
        'displayname': meta.displayName,
        'password': meta.password
    }
    response = requests.post(url=url, json=body)
    if response.status_code != 200:
        raise HTTPException(detail=str(response.text), status_code=response.status_code)
    data = response.json()
    
    id_smd = data.get('_id')
    nama = data.get('username')
    email = data.get('email')
    
    user = await userdata.filter(email=email).first()
    
    global namaYangDisimpan
    if await cek_namaku_ada(nama=nama) == False:
        namaYangDisimpan = await set_name_unik(nama=nama)
    else:
        namaYangDisimpan = nama
    
    if user:
        
        if user.smdAuth is False:
            
            user.smdAuth = True
            
            if cek_admin is True:
                user.admin = True
                user.AtsumaruKanjo += 999999999
                user.NegaiGoto += 999999999
            else:
                user.AtsumaruKanjo += 100

            if user.nama is None:
                user.nama = namaYangDisimpan
            
            if user.smdID is None:
                user.smdID = id_smd
            
            await user.save()
        
        token = create_access_token(user=user)
        response = auth_response(user=user, token=token)
        return JSONResponse(content=response, status_code=200)
    
    else:
        
        if cek_admin(email=email) is False:
            save = userdata(nama=namaYangDisimpan, email=email, smdAuth=True, AtsumaruKanjo=100, smdID=id_smd)
        else:
            save = userdata(nama=namaYangDisimpan, email=email, smdAuth=True, AtsumaruKanjo=999999999, NegaiGoto=999999999, smdID=id_smd, admin=True)
        
        await save.save()
        
        user = await userdata.filter(email=email).first()
        
        token = create_access_token(user=user)
        
        response = auth_response(user=user, token=token)
        return JSONResponse(content=response, status_code=200)
