# Community Chat API
import codecs
from datetime import datetime
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException
from configs import config
from database.model import logpercakapan,logcommunitychat
from helper.fitur import obrolan, request_audio
from helper.translate import translate_target, translate_target_premium
from helper.access_token import check_access_token_expired, decode_access_token
from helper.response import pesan_response
from helper.premium import check_premium

router = APIRouter(prefix='/websoket/community-chat', tags=['Community-Chat-WEBSOCKET'])

# Dictionary to store connected WebSocket clients
connected_users = {}
        
@router.websocket('/chatting')
async def communityChatSocket(websocket: WebSocket, access_token: str):
    await websocket.accept()

    try:
        while True:
            permintaan = await websocket.receive_json()
            
            # check access_token setiap ws menerima json
            check = check_access_token_expired(access_token=access_token)
            if check is True:
                await websocket.close()
                break
            else:
                dataJWT = decode_access_token(access_token=access_token)
                email = dataJWT.get('sub')
                
            
            async def ChatRestore(msg_group: str):
                messages: list[logcommunitychat] = await logcommunitychat.filter(group=msg_group)
                
                for msg in messages:
                    message = {
                        "action": "ChatRestore",
                        "sender": msg.sender,
                        "group": msg.group,
                        "text": msg.text,
                        "withMedia": False, 
                    }
                    
                    if msg.media is not None:
                        message["withMedia"] = True
                        message["media"] = {
                            "type": msg.media_type
                        }
                        
                        await websocket.send_json(message)
                        await websocket.send_bytes(msg.media)
                        
                        
                    await websocket.send_json(message)
                
            if permintaan.get("action") == "LoginNotif":
                await websocket.send_json({
                    "action": "InitialData",
                    "credentials": {
                        "sub": dataJWT.get('sub'),
                        "level": "user"
                        },
                    "group_list": [
                        "war",
                        "peace",
                        "drinking",
                        "smoking"
                    ]
                })
                
                connected_users[email] = {
                    "ws": websocket,
                    "currentGroup": "default"
                }
                
                await ChatRestore(connected_users[email]["currentGroup"])
            
            if permintaan.get("action") == "Chat":
                if permintaan.get("withMedia") and permintaan["withMedia"] == True:                
                    media = await websocket.receive_bytes()
                    media_type = permintaan.get("media").get("type")
                    msg_group = permintaan.get("group")
                    
                    permintaan["sender"] = email
                    
                    for user, states in connected_users.items():
                        if states["currentGroup"] == msg_group:
                            await states["ws"].send_json(permintaan)
                            await states["ws"].send_bytes(media)
                    
                    await logcommunitychat(sender=email,text=permintaan.get("text"), group=msg_group,media_type=media_type,media=media).save()
                else:
                    permintaan["sender"] = email
                    msg_group = permintaan.get("group")
                    
                    for user, states in connected_users.items():
                        if states["currentGroup"] == msg_group:
                            await states["ws"].send_json(permintaan)
                    
                    await logcommunitychat(sender=email,text=permintaan.get("text"), group=msg_group).save()

            if permintaan.get("action") == "GroupChange":
                currentGroup = permintaan.get("currentGroup")
                
                connected_users[email]["currentGroup"] = currentGroup
                
                await ChatRestore(currentGroup)
    except WebSocketDisconnect or WebSocketException:
        del connected_users[email]
        print("Client disconnected")
        