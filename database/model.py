from tortoise.models import Model
from tortoise import fields
from datetime import datetime
import pytz

WIB = pytz.timezone('Asia/Jakarta')

# USER
class UserData(Model):
    email = fields.CharField(max_length=255, pk=True)
    nama = fields.CharField(max_length=255, null=True)
    status = fields.CharField(max_length=50)
    admin = fields.BooleanField(default=False, null=True)
    birth_date = fields.DateField(null=True)
    gender = fields.CharField(max_length=1, null=True)
    banned = fields.BooleanField(default=False)
    token = fields.CharField(max_length=255, null=True)
    timestamp = fields.DatetimeField()

    async def save(self, *args, **kwargs):    
        self.timestamp = datetime.now(WIB)
        await super().save(*args, **kwargs)

class UserPremium(Model):
    UUID_number = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.UserData', related_name='premium', on_delete=fields.CASCADE)
    token = fields.CharField(max_length=255, null=True)
    transaction_service = fields.CharField(max_length=255)
    timestamp = fields.DatetimeField()

    async def save(self, *args, **kwargs):    
        self.timestamp = datetime.now(WIB)
        await super().save(*args, **kwargs)

class UserAuth(Model):
    UUID_number = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.UserData', related_name='auth', on_delete=fields.CASCADE)
    password = fields.CharField(max_length=255, null=True)
    wso = fields.BooleanField(default=False)
    google = fields.BooleanField(default=False)
    smd = fields.BooleanField(default=False)

class UserGoogleAuth(Model):
    UUID_number = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.UserData', related_name='google_auth', on_delete=fields.CASCADE)
    drive_id = fields.CharField(max_length=255)
    access_token = fields.CharField(max_length=255)
    refresh_token = fields.CharField(max_length=255)
    token_exp = fields.DatetimeField()

class UserAsset(Model):
    UUID_number = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.UserData', related_name='asset', on_delete=fields.CASCADE)
    NegaiGoto = fields.IntField()
    AtsumaruKanjo = fields.IntField()
    character = fields.JSONField()

# FITUR
class BWResult(Model):
    UUID_number = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.UserData', related_name='bw_result', on_delete=fields.CASCADE)
    ID_number = fields.IntField()
    timestamp = fields.DatetimeField()
    character = fields.CharField(max_length=255)
    transcript = fields.TextField()
    translation = fields.TextField()
    audio_url = fields.CharField(max_length=255)

    async def save(self, *args, **kwargs):    
        self.timestamp = datetime.now(WIB)
        await super().save(*args, **kwargs)

class AIUHistory(Model):
    UUID_number = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.UserData', related_name='aiu_history', on_delete=fields.CASCADE)
    ID_number = fields.IntField()
    timestamp = fields.DatetimeField()
    character = fields.CharField(max_length=255)
    user_input = fields.TextField()
    japanese_output = fields.TextField()
    display_output = fields.TextField()
    service = fields.CharField(max_length=255)
    audio_url = fields.CharField(max_length=255)

    async def save(self, *args, **kwargs):    
        self.timestamp = datetime.now(WIB)
        await super().save(*args, **kwargs)

class AudioData(Model):
    UUID_number = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.UserData', related_name='audio_data', on_delete=fields.CASCADE)
    character = fields.CharField(max_length=255)
    japanese_text = fields.TextField(null=True)
    audio_data = fields.BinaryField()
    service = fields.CharField(max_length=50)

class DWResult(Model):
    UUID_number = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.UserData', related_name='dw_result', on_delete=fields.CASCADE)
    timestamp = fields.DatetimeField()
    result = fields.BinaryField()
    shape = fields.CharField(max_length=255)
    prompt = fields.TextField()

    async def save(self, *args, **kwargs):    
        self.timestamp = datetime.now(WIB)
        await super().save(*args, **kwargs)

class PityCounter(Model):
    UUID_number = fields.UUIDField(pk=True)
    ID_number = fields.IntField()
    user = fields.ForeignKeyField('models.UserData', related_name='pity_counter', on_delete=fields.CASCADE)
    timestamp = fields.DatetimeField()
    obtained = fields.BooleanField(default=False)
    limited = fields.BooleanField(default=False)
    four_star_counter = fields.IntField()
    five_star_counter = fields.IntField()
    bonus_counter = fields.IntField()

    async def save(self, *args, **kwargs):    
        self.timestamp = datetime.now(WIB)
        await super().save(*args, **kwargs)

# DATA SYSTEM
class KarakterListWSO(Model):
    ID_number = fields.IntField(pk=True)
    nama = fields.CharField(max_length=255)
    variant = fields.CharField(max_length=255)
    rarity = fields.CharField(max_length=255)
    limited = fields.BooleanField(default=False)
    deskripsi = fields.TextField()
    release_time = fields.DatetimeField()
    endtime = fields.DatetimeField()
    asset = fields.CharField(max_length=255)

class HookListService(Model):
    UUID_number = fields.UUIDField(pk=True)
    tujuan = fields.CharField(max_length=255)
    service = fields.CharField(max_length=255)

# COMMUNITY
class CommunityList(Model):
    UUID_number = fields.UUIDField(pk=True)
    nama = fields.CharField(max_length=255)
    type = fields.CharField(max_length=255)
    deskripsi = fields.TextField()
    profile_photo = fields.CharField(max_length=255)
    creator = fields.CharField(max_length=255)
    member = fields.TextField()
    requests = fields.JSONField()

class CommunityChatHistory(Model):
    UUID_number = fields.UUIDField(pk=True)
    community = fields.ForeignKeyField('models.CommunityList', related_name='chat_history', on_delete=fields.CASCADE)
    sender = fields.CharField(max_length=255)
    timestamp = fields.DatetimeField()
    message = fields.TextField()
    media = fields.BinaryField(max_length=255)
    media_type = fields.CharField(max_length=50)

    async def save(self, *args, **kwargs):    
        self.timestamp = datetime.now(WIB)
        await super().save(*args, **kwargs)

# TRANSAKSI
class HallOfSupport(Model):
    UUID_number = fields.UUIDField(pk=True)
    transaction_id = fields.CharField(max_length=255)
    timestamp = fields.DatetimeField()
    service = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    nama = fields.CharField(max_length=255)
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    currency = fields.CharField(max_length=10)

    async def save(self, *args, **kwargs):    
        self.timestamp = datetime.now(WIB)
        await super().save(*args, **kwargs)

class AnonimBuyer(Model):
    UUID_number = fields.UUIDField(pk=True)
    service = fields.CharField(max_length=255)
    timestamp = fields.DatetimeField()
    email = fields.CharField(max_length=255)
    nama = fields.CharField(max_length=255)
    phone_number = fields.CharField(max_length=255)
    object = fields.CharField(max_length=255)
    jumlah = fields.DecimalField(max_digits=10, decimal_places=2)
    currency = fields.CharField(max_length=10)

    async def save(self, *args, **kwargs):    
        self.timestamp = datetime.now(WIB)
        await super().save(*args, **kwargs)
