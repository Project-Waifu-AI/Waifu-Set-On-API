from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from body_request.auth_body_request import smd_login, smd_register
from database.model import userdata
from helping.auth_helper import create_access_token, apakahNamakuAda, buatNamaUnik, cek_admin
import requests
import json

router = APIRouter(prefix='/auth/smd', tags=['SMD AUTH'])

API_SMD_DOMAIN_AUTH = 'https://663d-103-105-55-169.ngrok-free.app/api/auth/'

@router.post('/login')
async def authLogin(meta: smd_login):
    endpoint = 'login'
    try:
        url = f'{API_SMD_DOMAIN_AUTH}{endpoint}'
        
        body = {
            'username': meta.username,
            'password': meta.password
        }
        
        response = requests.post(url=url, json=body)
        data = response.json()
        id_smd = data.get('_id')
        nama = data.get('username')
        email = data.get('email')
        
        user = await userdata.filter(email=email).first()
        
        global namaYangDisimpan
        if await apakahNamakuAda(nama=nama) == False:
            namaYangDisimpan = await buatNamaUnik(nama=nama)
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
            return JSONResponse(content={
                'access_token': token,
                'google_auth': str(user.googleAuth),
                'akunWSO': str(user.akunwso)
            }, status_code=200)
        
        else:
            
            if cek_admin(email=email) is False:
                save = userdata(nama=namaYangDisimpan, email=email, smdAuth=True, AtsumaruKanjo=100, smdID=id_smd)
            else:
                save = userdata(nama=namaYangDisimpan, email=email, smdAuth=True, AtsumaruKanjo=999999999, smdID=id_smd, admin=True)
            
            await save.save()
            
            user = await userdata.filter(email=email).first()
            
            token = create_access_token(user=user)
            
            return JSONResponse(content={
                'access_token': token,
                'google_auth': str(save.googleAuth),
                'akunWSO': str(save.akunwso)
            })
            
    except Exception as e:
        raise HTTPException(detail='somthing went wrong', status_code=500)
    
    
@router.post('/register')
async def authRegister(meta: smd_register):
    endpoint = 'register'
    try:
        url = f'{API_SMD_DOMAIN_AUTH}{endpoint}'
        body = {
            'username': meta.username,
            'email': meta.email,
            'displayname': meta.displayName,
            'password': meta.password
        }
        response = requests.post(url=url, json=body)
        data = response.json()
        
        id_smd = data.get('_id')
        nama = data.get('username')
        email = data.get('email')
        
        user = await userdata.filter(email=email).first()
        
        global namaYangDisimpan
        if await apakahNamakuAda(nama=nama) == False:
            namaYangDisimpan = await buatNamaUnik(nama=nama)
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
            return JSONResponse(content={
                'access_token': token,
                'google_auth': str(user.googleAuth),
                'akunWSO': str(user.akunwso)
            }, status_code=200)
        
        else:
            
            if cek_admin(email=email) is False:
                save = userdata(nama=namaYangDisimpan, email=email, smdAuth=True, AtsumaruKanjo=100, smdID=id_smd)
            else:
                save = userdata(nama=namaYangDisimpan, email=email, smdAuth=True, AtsumaruKanjo=999999999, smdID=id_smd, admin=True)
            
            await save.save()
            
            user = await userdata.filter(email=email).first()
            
            token = create_access_token(user=user)
            
            return JSONResponse(content={
                'access_token': token,
                'google_auth': str(save.googleAuth),
                'akunWSO': str(save.akunwso)
            })
            
    except Exception as e:
        raise HTTPException(detail='somthing went wrong', status_code=500)