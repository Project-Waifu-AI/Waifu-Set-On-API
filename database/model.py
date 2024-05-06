from tortoise.models import Model
from tortoise import fields

# LOG 
class logaudio(Model):
    audio_id = fields.IntField()
    email = fields.CharField(max_length=320)
    transcript = fields.CharField(max_length=225)
    translate = fields.CharField(max_length=225)
    karakter = fields.CharField(max_length=225)

    class Meta:
        table = "logaudio"
    
    def __str__(self):
        return self.audio_id

class logpercakapan(Model):
    id_percakapan = fields.IntField()
    karakter = fields.CharField(max_length=225)
    email = fields.CharField(max_length=320)
    input = fields.CharField(max_length=225)
    output = fields.TextField()
    translate = fields.CharField(max_length=225)

    class Meta:
        table = "logpercakapan"
    
    def __str__(self):
        return self.id_percakapan

class logdelusion(Model):
    delusion_id = fields.IntField()
    email = fields.CharField(max_length=320)
    delusion_prompt = fields.CharField(max_length=225)
    delusion_shape = fields.CharField(max_length=100)
    delusion_result = fields.BinaryField() 
    
    class Meta:
        table = 'logdelusion'
        
    def __str__(self):
        return self.email

# token dan refresh_token autentikasi tambahan
class token_google(Model):
    email = fields.CharField(max_length=320)
    access_token = fields.CharField(max_length=255)
    token_exp = fields.DatetimeField()
    refersh_token = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'token_google'

    def __str__(self):
        return self.email

# USER & KARAKTER DATA
class userdata(Model):
    email = fields.CharField(max_length=320, pk=True)
    nama = fields.CharField(max_length=225, null=True)
    status = fields.CharField(max_length=225, null=True)
    admin = fields.BooleanField(default=False)
    ulang_tahun = fields.DateField(null=True)
    gender = fields.CharField(max_length=10, null=True)
    password = fields.BinaryField(max_length=225,null=True)
    AtsumaruKanjo = fields.IntField(default=0)
    NegaiGoto = fields.IntField(default=0)
    pity_4_star = fields.IntField(default=0)
    pity_5_star = fields.IntField(default=0)
    gacha_count = fields.IntField(default=0)
    karakterYangDimiliki = fields.JSONField(default=[])
    wsoAuth = fields.BooleanField(default=False)
    googleAuth = fields.BooleanField(default=False)
    smdAuth = fields.BooleanField(default=False)
    driveID = fields.CharField(null=True, max_length=320)
    smdID = fields.CharField(null=True, max_length=320)
    token_konfirmasi = fields.CharField(max_length=225, null=True)
    premium_token = fields.CharField(max_length=225, null=True)
    ban = fields.BooleanField(default=False)

    class Meta:
        table = "userdata"

    def __str__(self):
        return self.email

class anonim_buyer(Model):
    id_transaksi = fields.CharField(max_length=320)
    service = fields.CharField(max_length=100)
    email = fields.CharField(max_length=225)
    nama = fields.CharField(max_length=225, null=True)
    no_telp = fields.CharField(max_length=225, null=True)
    object_buy = fields.CharField(max_length=225)
    nominal = fields.IntField()
    currency = fields.CharField(max_length=100)
    waktu = fields.DatetimeField()

    class Meta:
        tables = 'anonimn_buyer'

    def __str__(self):
        return self.id_transaksi

class hall_of_support(Model):
    id_transaksi = fields.CharField(max_length=335)
    service = fields.CharField(max_length=100)
    email = fields.CharField(max_length=225, null=True)
    nama = fields.CharField(max_length=225, null=True)
    pesan = fields.CharField(max_length=225, null=True)
    nominal = fields.IntField()
    currency = fields.CharField(max_length=100)
    waktu = fields.DatetimeField()
    
    class Meta:
        tables = 'anonimn_buyer'

    def __str__(self):
        return self.email
    
class KarakterData(Model):
    nama = fields.CharField(max_length=225, pk=True)
    bahasaYangDigunakan = fields.CharField(max_length=225)
    informasi_tambahan = fields.JSONField(null=True)
    speakerID = fields.JSONField(null=True)
    
    class Meta:
        table = 'karakter'
    
    def __str__(self):
        return self.nama
    
class GachaHistory(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.userdata', related_name='gacha_history')
    characters = fields.JSONField()
    limited = fields.BooleanField()
    timestamp = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "gachahistory"