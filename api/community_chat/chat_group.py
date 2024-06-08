import uuid
from fastapi import APIRouter, File, HTTPException, Header, Response, UploadFile,status
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
from handler.request.cc_body_request import ChatCommunity
import base64
import io
from PIL import Image
from handler.request.dw_body_request import CreateDelusion, VariantDelusion
from helper.premium import check_premium
from helper.fitur import generateDelusion, generateDelusionVariant
from helper.cek_and_set import cek_kalimat_promting, cek_and_set_ukuran_delusion, set_response_save_delusion
from database.model import logdelusion,communitylist,logcommunitychat,userdata
from helper.access_token import check_access_token_expired, decode_access_token
from configs import config
from tortoise.exceptions import DoesNotExist
import time
from handler.response.response import error_response, success_response, cc_response

router = APIRouter(prefix='/chat',tags=['Community-Chat'])

@router.post("/create")
async def create_community(community: ChatCommunity, access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    community_id = str(uuid.uuid4())
    community_type = community.community_type
    valid_community_type = ["default", "private", "all"]
    community_member = []
    
    if community_type not in valid_community_type:
        raise HTTPException(status_code=403, detail=error_response("Please enter valid community type", "Invalid input type", "create-chat", email))
    
    if community_type in ["private", "all"]:
        community_member = [email]
    
    if community_type == "default" and payloadJWT.get("level") == "user":
        raise HTTPException(status_code=401, detail=error_response("You do not have permission to create default community!", "Insufficient user level", "create-chat", email))
    
    if community_type == "default":
        members = await userdata.all()
        member_list = []
        
        for member in members:
            member_list.append(member.email)
        
        community_member = member_list
    
    permintaan = None
    if community_type == "private":
        permintaan = []
    
    new_community = communitylist(id=community_id,community_name=community.community_name,community_type=community_type,community_desc=community.community_desc,community_member=community_member,created_by = email, permintaan = permintaan)
    
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
    }, status_code=201)

@router.put('/join-community')
async def join_community(community_id: str,access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    community_to_join = await communitylist.filter(id=community_id).first()
    if not community_to_join:
        raise HTTPException(status_code=404, detail=error_response("Community Not Found", "Object does not exist", "join-community-chat", email))
        
    community_members = community_to_join.community_member
    if email in community_members:
        raise HTTPException(status_code=405, detail=error_response("You already join the community", "Already joined", "join-community-chat", email))
    
    community_members.append(email)
    await community_to_join.save()
    
    return JSONResponse(success_response("join-community-chat", f"Successfully join community {community_to_join.community_name}", email), status_code=201)

@router.post("/join-private-community")
async def join_private_community(community_id: str, acceptance_reason: str, access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    community_to_join = await communitylist.filter(id=community_id).first()
    if not community_to_join:
        raise HTTPException(status_code=404, detail=error_response("Community Not Found", "Object does not exist", "join-private-community-chat", email))
        
    community_members = community_to_join.community_member
    if email in community_members:
        raise HTTPException(status_code=405, detail=error_response("You already join the community", "Already joined", "join-private-community-chat", email))
    
    join_requests = community_to_join.permintaan
   
    for join_req in join_requests:
        if email == join_req.get("email"):
            raise HTTPException(status_code=405, detail=error_response("You already requested to join the community. Please wait!", "Already requested", "join-private-community-chat", email))
    
    join_requests.append({
        "email": email,
        "acceptance_reason": acceptance_reason,
        "timestamps": time.time()
    })
    
    await community_to_join.save()
    
    return JSONResponse(success_response("join-private-community-chat", f"request to join community with id: {community_id} have been sent!", email), status_code=201)

@router.get("/get-join-requests")
async def get_join_request(access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    owned_community_list: list[communitylist] = await communitylist.filter(created_by=email)
    
    join_request_list: list = []
    
    for owned_community in owned_community_list:
        for join_req in owned_community.permintaan:
            join_request_list.append({
                "email": join_req.get("email"),
                "community_name": owned_community.community_name,
                "community_id": owned_community.id,
                "acceptance_reason": join_req.get("acceptance_reason"),
                "timestamps": join_req.get("timestamps"),
            })   
    
    return JSONResponse(join_request_list, status_code=200)

@router.put("/handle-join-request")
async def handle_join_request(community_id: str, requesting_email: str, is_accepted: bool,access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    requested_community: communitylist = await communitylist.filter(id=community_id).first()
    req_email_list = []
    for join_req in requested_community.permintaan:
        req_email_list.append(join_req.get("email"))
        
    if requesting_email not in req_email_list:
        raise HTTPException(status_code=404, detail=error_response("Join request not found", "Object does not exist", "handle-join-request-chat", email))
        
    if is_accepted:
        # acc user request and add them to desired community
        requested_community.community_member.append(requesting_email)
        # remove join request
        updated_permintaan = [d for d in requested_community.permintaan if d["email"] != requesting_email]
        requested_community.permintaan = updated_permintaan
        await requested_community.save()
        
        return JSONResponse({
            "status": "join request accepted",
            "added_email": requesting_email,
            "to_community": requested_community.community_name
        }, status_code=201)
    else:
        updated_permintaan = [d for d in requested_community.permintaan if d["email"] != requesting_email]
        requested_community.permintaan = updated_permintaan
        await requested_community.save()
        
        return JSONResponse({
            "status": "join request denied",
            "denied_email": requesting_email
        })

@router.get("/get")
async def get_community_list(access_token: str = Header(...), joined_only: bool = False):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    community_list = await communitylist.all()
    response: list[dict] = []
    for community in community_list:
        members = community.community_member
        if joined_only:
            if email in members:
                response.append(cc_response(community.id, community.community_name, community.community_type, community.community_desc, members, community.created_by))
        else:
            response.append(cc_response(community.id, community.community_name, community.community_type, community.community_desc, members, community.created_by))
        
    return JSONResponse(response, status_code=200)

@router.get("/get-community-info")
async def get_community_info(community_id: str, access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    try:
        requested_community = await communitylist.get(id=community_id)
        
        return JSONResponse(cc_response(requested_community.id, requested_community.community_name, requested_community.community_type, requested_community.community_desc, requested_community.community_member, requested_community.created_by), status_code=200)
    except DoesNotExist  as e:
        raise HTTPException(status_code=404, detail=error_response("Community Not Found", str(e), "get-chat-community", email))
    
@router.put("/update-info")
async def update_community_info(community_info: ChatCommunity, community_id: str,access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    try:
        community_to_update = await communitylist.get(id=community_id)
    
        community_to_update.community_name = community_info.community_name
        community_to_update.community_desc = community_info.community_desc
        
        await community_to_update.save()
        
        return JSONResponse({
            "status": "ok",
            "updated_community": {
                "community_id": community_id,
                "community_name": community_info.community_name,
            }
        }, status_code=201)
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=error_response("Community Not Found", str(e), "update-info-chat", email))           

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
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
    
    try:
        community_to_search: communitylist = await communitylist.get(id=community_id)
        community_pp = community_to_search.community_pp
        
        
        if community_pp is not None:
            image_data = base64.b64decode(community_pp)
            return StreamingResponse(io.BytesIO(image_data), media_type="image/png")
        else:
            raise HTTPException(status_code=404, detail=error_response("Community Profile Photo Not Found", "Object does not exist", "get-photo-profile-chat", email))
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=error_response("Community Not Found", str(e), "get-photo-profile-chat", email))
        
@router.put("/update-photo-profile")
async def update_photo_profile(community_id: str, profile_pict: UploadFile = File(...), access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    try:
        if "image" not in profile_pict.content_type:
            raise HTTPException(status_code=404, detail=error_response("Please upload a valid image file", "Invalid Input Type", "update-photo-profile-chat", email))
                
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
            }, status_code=201)
            
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=error_response("Community Not Found", "Object does not exist", "update-photo-profile-chat", email))

@router.delete("/delete-photo-profile")
async def delete_photo_profile(community_id: str, access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
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
            }, status_code=200)
            
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=error_response("Community Not Found", str(e), "delete-photo-profile-chat", email))
            
@router.delete("/delete")
async def delete_community(community_id: str, access_token: str = Header(...)):
    # credential checking
    check = check_access_token_expired(access_token=access_token)

    if check is True:
        return RedirectResponse(url=config.redirect_uri_page_masuk, status_code=300)
    else:
        payloadJWT = decode_access_token(access_token=access_token)
        email = payloadJWT.get('sub')
        
    try:
        community_to_delete = await communitylist.get(id=community_id)
        deleted_community_name = community_to_delete.community_name
        
        await community_to_delete.delete()
        
        return JSONResponse({
            "status": "ok",
            "deleted_community": deleted_community_name
        }, status_code=200)
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=error_response("Community Not Found", str(e), "delete-chat", email))