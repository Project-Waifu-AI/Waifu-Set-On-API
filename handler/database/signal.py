from tortoise.signals import post_save
from database.model import UserData, UserAuth, UserAsset, UserGoogleAuth

@post_save(UserData)
async def create_related_records(sender, instance: UserData, created):
    if created:
        
        if instance.admin is True:
            await UserAsset.create(user=instance, negai_goto=999999999, atsumaru_kanjo=999999999, character={'all-char'})
        
        else:
            await UserAsset.create(user=instance, negai_goto=0, atsumaru_kanjo=800, character={'default-char'})