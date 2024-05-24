import uuid
from fastapi import APIRouter, File, HTTPException, Header, Response, UploadFile,status
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
from body_request.cc_group_request import ChatCommunity
import base64
import io
from PIL import Image
from body_request.dw_body_request import CreateDelusion, VariantDelusion
from helper.premium import check_premium
from helper.fitur import generateDelusion, generateDelusionVariant
from helper.cek_and_set import cek_kalimat_promting, cek_and_set_ukuran_delusion, set_response_save_delusion
from database.model import logdelusion,communitylist,logcommunitychat,userdata,privatecommunityjoinreq
from helper.access_token import check_access_token_expired, decode_access_token
from configs import config
from tortoise.exceptions import DoesNotExist

router = APIRouter(prefix='/chat',tags=['Community-Chat'])

@router.post("/create")
async def create_community(community: ChatCommunity, access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    community_id = str(uuid.uuid4())
    community_type = community.community_type
    valid_community_type = ["default", "private", "all"]
    community_member = []
    
    if community_type not in valid_community_type:
        return JSONResponse({
            "msg": "Please enter valid community type"
        }, status_code=status.HTTP_400_BAD_REQUEST)
    
    if community_type in ["private", "all"]:
        community_member = [email]
    
    if community_type == "default" and payloadJWT.get("level") == "user":
        return JSONResponse({
            "msg": "You do not have permission to create default community!"
        }, status_code=status.HTTP_403_FORBIDDEN)
    
    if community_type == "default":
        members = await userdata.all()
        member_list = []
        
        for member in members:
            member_list.append(member.email)
        
        community_member = member_list
    
    new_community = communitylist(id=community_id,community_name=community.community_name,community_type=community_type,community_desc=community.community_desc,community_member=community_member,created_by = email)
    
    await new_community.save()
    
    return JSONResponse({
        "status": "ok",
        "created_community": {
            "community_name": community.community_name,
            "community_type": community.community_type,
            "community_desc": community.community_desc,
            "community_member": community_member,
            "created_by": email
        }
    }, status_code=status.HTTP_201_CREATED)

@router.put('/join-community')
async def join_community(community_id: str,access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    community_to_join = await communitylist.filter(id=community_id).first()
    if not community_to_join:
        return JSONResponse({
            "error": "Community Not Found"
        }, status_code=status.HTTP_404_NOT_FOUND)
        
    community_members = community_to_join.community_member
    if email in community_members:
        return JSONResponse({
            "error": "You already join the community"
        }, status_code=status.HTTP_400_BAD_REQUEST)
    
    community_members.append(email)
    await community_to_join.save()
    
    return JSONResponse({
        "msg": f"Successfully join community {community_to_join.community_name}"
    }, status_code=status.HTTP_201_CREATED)

@router.post("/join-private-community")
async def join_private_community(community_id: str,access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    community_to_join = await communitylist.filter(id=community_id).first()
    if not community_to_join:
        return JSONResponse({
            "error": "Community Not Found"
        }, status_code=status.HTTP_404_NOT_FOUND)
        
    community_members = community_to_join.community_member
    if email in community_members:
        return JSONResponse({
            "error": "You already join the community"
        }, status_code=status.HTTP_400_BAD_REQUEST)
    
    is_user_already_request = await privatecommunityjoinreq.filter(email=email).first()
    if is_user_already_request:
        return JSONResponse({
            "error": "You already requested to join the community. Please wait!"
        }, status_code=status.HTTP_400_BAD_REQUEST)
    
    await privatecommunityjoinreq(email=email, requested_community_id=community_id).save()
    
    return JSONResponse({
        "msg": f"request to join community with id {community_id} have been sent!"
    }, status_code=status.HTTP_201_CREATED)

@router.get("/get-join-request")
async def get_join_request(access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    community_list: list[communitylist] = await communitylist.all()
    owned_community_id = []
    for community in community_list:
        if email in community.community_member:
            owned_community_id.append(community.id)
            
    join_request_list: list[privatecommunityjoinreq] = await privatecommunityjoinreq.raw(f"select * from privatecommunityjoinreq where requested_community_id IN {tuple(owned_community_id)}")
    
    response = []
    for join_request in join_request_list:
        response.append({
            "request_id": join_request.id,
            "email": join_request.email,
            "requested_community_id": join_request.requested_community_id,
            "requested_at": str(join_request.requested_at)
        })
    
    return JSONResponse(response, status_code=status.HTTP_200_OK)

@router.put("/handle-join-request")
async def handle_join_request(request_id: str, is_accepted: bool,access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    join_req = await privatecommunityjoinreq.filter(id=request_id).first()
    
    if not join_req:
        return JSONResponse({
            "error": "Join request not found"
        }, status_code=status.HTTP_404_NOT_FOUND)
        
    if is_accepted:
        # acc user request and add them to desired community
        requested_community = await communitylist.filter(id=join_req.requested_community_id).first()
        
        requested_community.community_member.append(join_req.email)
        
        await requested_community.save()
        await join_req.delete()
        return JSONResponse({
            "status": "join request accepted",
            "added_email": join_req.email,
            "to_community": requested_community.community_name
        }, status_code=status.HTTP_201_CREATED)
    else:
        await join_req.delete()
        return JSONResponse({
            "status": "join request denied",
            "denied_email": join_req.email
        })

@router.get("/get")
async def get_community_list(access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=status.HTTP_401_UNAUTHORIZED)
        
    community_list = await communitylist.all()
    response: list[dict] = []
    for community in community_list:
        response.append({
            "community_id": community.id,
            "community_name": community.community_name,
            "community_type": community.community_type,
            "community_desc": community.community_desc,
            "community_member": community.community_member,
        })
    
    return JSONResponse(response, status_code=status.HTTP_200_OK)

@router.get("/get-community-info")
async def get_community_info(community_id: str, access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=status.HTTP_401_UNAUTHORIZED)
    
    try:
        requested_community = await communitylist.get(id=community_id)
        
        return JSONResponse({
            "community_name": requested_community.community_name,
            "community_desc": requested_community.community_desc,
            "community_member": requested_community.community_member,
            "created_by": requested_community.created_by
        }, status_code=status.HTTP_200_OK)
    except DoesNotExist:
        return JSONResponse({
            "Error": "Community Not Found"
        }, status_code=status.HTTP_404_NOT_FOUND)
    
@router.put("/update-community-info")
async def update_community_info(community_info: ChatCommunity, community_id: str,access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=status.HTTP_401_UNAUTHORIZED)
    
    try:
        community_to_update = await communitylist.get(id=community_id)
    
        community_to_update.community_name = community_info.community_name
        community_to_update.community_desc = community_info.community_desc
        community_to_update.community_member = community_info.community_member
        
        await community_to_update.save()
        
        return JSONResponse({
            "status": "ok",
            "updated_community": {
                "community_id": community_id,
                "community_name": community_info.community_name,
            }
        }, status_code=status.HTTP_201_CREATED)
    except DoesNotExist:
        return JSONResponse({
            "Error": "Community Not Found"
        }, status_code=status.HTTP_404_NOT_FOUND)
            

@router.get(
    "/get-photo-profile",
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
    response_class=Response
)
async def get_community_photo_profile(community_id: str, access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=status.HTTP_401_UNAUTHORIZED)
    
    try:
        community_to_search: communitylist = await communitylist.get(id=community_id)
        community_pp = community_to_search.community_pp
        
        
        if community_pp is not None:
            image_data = base64.b64decode(community_pp)
            return StreamingResponse(io.BytesIO(image_data), media_type="image/png")
        else:
            return JSONResponse({
                "status": "Community Profile Photo Not Found"
            }, status_code=status.HTTP_404_NOT_FOUND)
        
            
    except DoesNotExist:
        return JSONResponse({
            "Error": "Community Not Found"
        }, status_code=status.HTTP_404_NOT_FOUND)
        
@router.put("/update-photo-profile")
async def update_photo_profile(community_id: str, profile_pict: UploadFile = File(...), access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=status.HTTP_401_UNAUTHORIZED)
    
    try:
        if "image" not in profile_pict.content_type:
            return JSONResponse({
                "Error": "Please upload a valid image file"
            }, status_code=status.HTTP_403_FORBIDDEN)
                
        community_to_update: communitylist = await communitylist.get(id=community_id)
        community_to_update.community_pp = await profile_pict.read()
        
        # save updated profile pict
        await community_to_update.save()
        
        return JSONResponse({
                "status": "ok",
                "updated_community_pp": {
                    "community_id": community_id,
                    "community_name": community_to_update.community_name
                }
            }, status_code=status.HTTP_201_CREATED)
            
    except DoesNotExist:
        return JSONResponse({
            "Error": "Community Not Found"
        }, status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/delete-photo-profile")
async def delete_photo_profile(community_id: str, access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=status.HTTP_401_UNAUTHORIZED)
    
    try:        
        group_to_update: communitylist = await communitylist.get(id=community_id)
        group_to_update.community_pp = None
        
        # save updated profile pict
        await group_to_update.save()
        
        return JSONResponse({
                "status": "ok",
                "deleted_community_pp": {
                    "community_id": community_id,
                    "community_name": group_to_update.community_name
                }
            }, status_code=status.HTTP_201_CREATED)
            
    except DoesNotExist:
        return JSONResponse({
            "Error": "Community Not Found"
        }, status_code=status.HTTP_404_NOT_FOUND)
            
@router.delete("/delete")
async def delete_community(community_id: str, access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=status.HTTP_401_UNAUTHORIZED)
    
    try:
        community_to_delete = await communitylist.get(id=community_id)
        deleted_community_name = community_to_delete.community_name
        
        await community_to_delete.delete()
        
        return JSONResponse({
            "status": "ok",
            "deleted_community": deleted_community_name
        }, status_code=status.HTTP_202_ACCEPTED)
    except DoesNotExist:
        return JSONResponse({
            "Error": "Community Not Found"
        }, status_code=status.HTTP_404_NOT_FOUND)