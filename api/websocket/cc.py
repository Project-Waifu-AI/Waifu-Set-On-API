# Community Chat API
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException
from database.model import logcommunitychat
from helper.access_token import check_access_token_expired, decode_access_token
import requests

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
                
            
            async def ChatRestore(msg_group_id: str):
                messages: list[logcommunitychat] = await logcommunitychat.filter(community_id=msg_group_id)
                
                for msg in messages:
                    message = {
                        "action": "ChatRestore",
                        "sender": msg.sender,
                        "group_id": msg.community_id,
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
                # Define API endpoint URL

                # Set headers
                headers = {
                    "access-token": access_token  # Replace with your actual access token
                }

                # Send GET request
                all_group_list: list[dict] = requests.get(f"http://localhost:8081/api/chat/get", headers=headers).json()
                joined_group_list: list[dict] = requests.get(f"http://localhost:8081/api/chat/get?joined_only={True}", headers=headers).json()
                
                await websocket.send_json({
                    "action": "InitialData",
                    "credentials": {
                        "sub": dataJWT.get('sub'),
                        "level": dataJWT.get('level')
                        },
                    "joined_group_list": joined_group_list,
                    "all_group_list": all_group_list
                })
                
                connected_users[email] = {
                    "ws": websocket,
                    "currentGroup": joined_group_list[0]["community_id"]
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
                    
                    await logcommunitychat(sender=email,text=permintaan.get("text"), community_id=msg_group,media_type=media_type,media=media).save()
                else:
                    permintaan["sender"] = email
                    msg_group = permintaan.get("group")
                    
                    for user, states in connected_users.items():
                        if states["currentGroup"] == msg_group:
                            await states["ws"].send_json(permintaan)
                    
                    await logcommunitychat(sender=email,text=permintaan.get("text"), community_id=msg_group).save()

            if permintaan.get("action") == "GroupChange":
                currentGroupId = permintaan.get("currentGroup")
                
                connected_users[email]["currentGroup"] = currentGroupId
                
                await ChatRestore(currentGroupId)

            if permintaan.get("action") == "JoinRequest":
                headers = {
                    "access-token": access_token  # Replace with your actual access token
                }
                
                # create join request to server
                join_request_response = requests.post(f"http://localhost:8081/api/chat/join-private-community?community_id={permintaan.get('community_id')}", headers=headers)
                
                requested_community_info = requests.get(f"http://localhost:8081/api/chat/get-community-info?community_id={permintaan.get('community_id')}", headers=headers).json()
                json_join_req = join_request_response.json()
                
                
                
                if join_request_response.status_code == 201:
                    for admin in json_join_req["requested_to"]:
                        if admin in connected_users:
                            await connected_users[admin]["ws"].send_json({
                            "action": "JoinRequest",
                            "email": email,
                            "community_id": permintaan.get('community_id'),
                            "community_name": requested_community_info.get("community_name")
                        })
                
                await connected_users[email]["ws"].send_json({
                    "action": "JoinReqReponse",
                    "response": json_join_req
                })
    
            if permintaan.get("action") == "JoinRequestResponse":
                isRequestAccepted = permintaan.get("isRequestAccepted")
                data = permintaan.get("data")
                join_requests = requests.get(f"http://localhost:8081/api/chat/get-join-request", headers=headers).json()
                headers = {
                    "access-token": access_token  # Replace with your actual access token
                }
                
                join_request_id = 0
                
                for join_req in join_requests:
                    if data.get("email") == join_req.get("email") and data.get("community_id") == join_req.get("requested_community_id"):
                        join_request_id = join_req.get("request_id")
                
                requests.put(f"http://localhost:8081/api/chat/handle-join-request?request_id={join_request_id}&is_accepted={isRequestAccepted}", headers=headers)
    except WebSocketDisconnect or WebSocketException:
        del connected_users[email]
        print("Client disconnected")
        