import random
from datetime import datetime
from database.model import userdata, GachaHistory, KarakterData
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from helper.access_token import check_access_token_expired, decode_access_token
from configs import config


# class Character:
#     def __init__(self, name, rarity):
#         self.name = name
#         self.rarity = rarity

#     def __str__(self):
#         return f"{self.name} ({self.rarity}★)"

# # karakter dibawah ini hanya untuk percobaan belum karakter yang akan di gacha nanti hanya untuk mengetes fungsi gacha
# limited_5_star_characters = [Character("Archon", 5), Character("Harbinger", 5)]
# limited_4_star_characters = [Character("Knight", 4), Character("Samurai", 4)]
# limited_3_star_characters = [Character("Warrior", 3), Character("Archer", 3)]

# non_limited_5_star_characters = [Character("Dragonborn", 5), Character("Celestial", 5)]
# non_limited_4_star_characters = [Character("Mage", 4), Character("Ranger", 4)]
# non_limited_3_star_characters = [Character("Soldier", 3), Character("Rogue", 3)]

async def get_character(limited=False, rarity=None):
    items= []
    if rarity is None:
        roll = random.randint(1, 100)
        if roll <= 5:
            rarity = 5
        elif roll <= 25:
            rarity = 4
        else:
            rarity = 3
    if rarity == 5:
        if limited: 
            # Get a specific limited item (you can modify this to suit your needs)
            limited_item = await KarakterData.get(name="testchar", is_limited=True)

            # Combine the limited item with non-limited items of the same rarity
            items = [limited_item] + [item for item in await KarakterData.filter(rarity=rarity, is_limited=False)]

        else:
            items = await KarakterData.filter(rarity=rarity, is_limited=False)
    else:
        items = await KarakterData.filter(rarity=rarity)

    if not items:
        raise Exception(f"No items found with rarity {rarity} and is_limited={limited}")
    
    return random.choice(items)


async def gacha_pull(email, times, limited=False):
    results = []
    pity_4_star = 0
    pity_5_star = 0
    user_data = await get_user_data(email)

    if user_data:
        pity_4_star = user_data.pity_4_star
        pity_5_star = user_data.pity_5_star

    for _ in range(times):
        character = get_character(limited)
        results.append(character)
        if character.rarity == 4:
            pity_4_star = 0
        else:
            pity_4_star += 1
        if character.rarity == 5:
            pity_5_star = 0
        else:
            pity_5_star += 1
        if pity_4_star == 10:
            results.append(get_character(limited, rarity=4))
            pity_4_star = 0
        if pity_5_star == 100:
            results.append(get_character(limited, rarity=5))
            pity_5_star = 0
    await add_to_history(email, results, limited)
    return results


async def add_to_history(email, characters, limited):
    user_data, _ = await userdata.get_or_create(email=email)

    character_names = [str(char) for char in characters]
    user_data.karakterYangDimiliki += character_names

    if limited:
        user_data.gacha_count += 1
    else:
        user_data.AtsumaruKanjo -= 1  # Assuming free currency is consumed for non-limited pulls

    for char in characters:
        if char.rarity == 4:
            user_data.pity_4_star = 0
        elif char.rarity == 5:
            user_data.pity_5_star = 0
        else:
            if limited:
                user_data.pity_4_star += 1
                user_data.pity_5_star += 1

    await user_data.save()

    await GachaHistory.create(
        user=user_data,
        characters=character_names,
        limited=limited
    )

async def get_user_data(email):
    user_data = await userdata.get_or_none(email=email)
    return user_data

async def get_gacha_history(email):
    user_data = await get_user_data(email)
    if user_data:
        history = await GachaHistory.filter(user=user_data).prefetch_related('user').order_by('-timestamp')
        return history
    return []

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def get_current_user(api_key: str = Depends(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token is required")

    check = check_access_token_expired(access_token=api_key)

    if check is True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token has expired")
    
    payload_jwt = decode_access_token(access_token=api_key)
    email = payload_jwt.get('sub')

    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")

    return email