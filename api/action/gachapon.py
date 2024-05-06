from fastapi import APIRouter, Depends, Header, HTTPException
from helper.gacha_logic import gacha_pull, get_user_data, get_gacha_history, get_current_user
from database.model import KarakterData, userdata

router = APIRouter(prefix='/gacha', tags=['gachapon system'])

@router.get("/karakteryangdimiliki")
async def get_obtained_characters(email: str = Depends(get_current_user)):
    user_data = await get_user_data(email)
    if user_data:
        return {"karakterYangDimiliki": user_data.karakterYangDimiliki}
    else:
        return {"message": "User not found"}
    
@router.get("/gacha/single/non-limited")
async def gacha_single_non_limited(email: str = Depends(get_current_user)):
    email = email
    results = await gacha_pull(email, 1, limited=False)
    return [str(char) for char in results]

@router.get("/gacha/multi/non-limited")
async def gacha_multi_non_limited(email: str = Depends(get_current_user)):
    email = email
    results = await gacha_pull(email, 10, limited=False)
    return [str(char) for char in results]

@router.get("/gacha/single/limited")
async def gacha_single_limited(email: str = Depends(get_current_user)):
    email = email
    results = await gacha_pull(email, 1, limited=True)
    return [str(char) for char in results]

@router.get("/gacha/multi/limited")
async def gacha_multi_limited(email: str = Depends(get_current_user)):
    email = email
    results = await gacha_pull(email, 10, limited=True)
    return [str(char) for char in results]

@router.get("/gacha/history")
async def gacha_history(email: str = Depends(get_current_user)):
    history = await get_gacha_history(email)
    return history