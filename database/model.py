from tortoise.models import Model
from tortoise import fields

# LOG 
class logaudio(Model):
    audio_id = fields.IntField()
    email = fields.CharField(max_length=320)
    transcript = fields.CharField(max_length=225)
    translate = fields.CharField(max_length=225)
    audio_streming = fields.CharField(max_length=225)
    audio_download = fields.CharField(max_length=225)

    class Meta:
        table = "logaudio"
    
    def __str__(self):
        return self.audio_id

class logpercakapan(Model):
    id_percakapan = fields.IntField()
    email = fields.CharField(max_length=320)
    input = fields.CharField(max_length=225)
    output = fields.TextField()
    translate = fields.CharField(max_length=225)
    audio_streming = fields.CharField(max_length=225)
    audio_download = fields.CharField(max_length=225) 

    class Meta:
        table = "logpercakapan"
    
    def __str__(self):
        return self.id_percakapan

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
    admin = fields.BooleanField(default=False)
    ulang_tahun = fields.DateField(null=True)
    gender = fields.CharField(max_length=10, null=True)
    password = fields.BinaryField(max_length=225,null=True)
    AtsumaruKanjo = fields.IntField(default=0)
    NegaiGoto = fields.IntField(default=0)
    karakterYangDimiliki = fields.JSONField(null=True)
    akunwso = fields.BooleanField(default=False)
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

class KarakterData(Model):
    nama = fields.CharField(max_length=225, pk=True)
    bahasaYangDigunakan = fields.CharField(max_length=225)
    informasi_tambahan = fields.JSONField(null=True)
    speakerID = fields.JSONField(null=True)
    class Meta:
        table = 'karakter'
    
    def __str__(self):
        return self.nama