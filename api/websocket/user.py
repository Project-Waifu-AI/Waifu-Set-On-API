from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from database.model import userdata
from helper.access_token import decode_access_token, check_access_token_expired
from helper.response import user_response

router = APIRouter(prefix='/websoket/user',tags=['USER-WEBSOCKET'])

@router.websocket('/root')
async def userStatus(websocket: WebSocket, access_token: str):
    await websocket.accept()
    try:
        while True:
            permintaan = await websocket.receive_json()
            
            print(permintaan)
            
            check = check_access_token_expired(access_token=access_token)
            dataJWT = decode_access_token(access_token=access_token)
            email = dataJWT.get('sub')
            user = await userdata.filter(email=email).first()
            if check is False:
                
                if permintaan['action'] == 'set-online':
                    if user != 'online':
                        user.status = 'online'
                        await user.save()
                    await websocket.send_json('online')
                
                elif permintaan['action'] == 'get-data':
                    response = user_response(user=user)
                    await websocket.send_json(response)
                    
                elif permintaan['action'] == 'delete':
                    await user.delete()
                    break
                
                elif permintaan['action'] == 'update':
                    if permintaan['data']['nama'] is not None:
                        user.nama = permintaan['data']['nama']
                    
                    if permintaan['data']['gender'] is not None:
                        if permintaan['data']['gender'] in ('pria', 'perempuan'):
                            user.gender = permintaan['data']['gender']
                    
                    if permintaan['data']['ulang_tahun'] is not None:
                        user.ulang_tahun = permintaan['data']['ulang_tahun']
                    
                    await user.save()    
                    await websocket.send_json('data berhasil di update')
                
                else:
                    user.status = 'offline'
                    await user.save()
                    break
            else:
                user.status = 'offline'
                await user.save()
                break
            
    except WebSocketDisconnect:
        if user:
            user.status = 'offline'
            await user.save()
        print('disconnect')