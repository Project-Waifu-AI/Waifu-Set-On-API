from tortoise.models import Model
from tortoise import fields

# LOG 
class logaudio(Model):
    audio_id = fields.IntField()
    user_id = fields.CharField(max_length=225)
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
    user_id = fields.CharField(max_length=225)
    input = fields.CharField(max_length=225)
    output = fields.TextField()
    translate = fields.CharField(max_length=225)
    audio_streming = fields.CharField(max_length=225)
    audio_download = fields.CharField(max_length=225) 

    class Meta:
        table = "logpercakapan"
    
    def __str__(self):
        return self.id_percakapan

# USER
class userdata(Model):
    user_id = fields.UUIDField(pk=True)
    nama = fields.CharField(max_length=225, null=True)
    admin = fields.BooleanField(default=False)
    ulang_tahun = fields.DateField(null=True)
    gender = fields.CharField(max_length=10, null=True)
    email = fields.CharField(max_length=225)
    password = fields.BinaryField(max_length=225,null=True)
    AtsumaruKanjo = fields.IntField(default=0)
    NegaiGoto = fields.IntField(default=0)
    karakterYangDimiliki = fields.JSONField(null=True)
    akunwso = fields.BooleanField(default=False)
    googleAuth = fields.BooleanField(default=False)
    token_konfirmasi = fields.CharField(max_length=225, null=True)
    premium_token = fields.CharField(max_length=225, null=True)
    ban = fields.BooleanField(default=False)

    class Meta:
        table = "userdata"

    def __str__(self):
        return self.user_id

class KarakterData(Model):
    nama = fields.CharField(max_length=225, pk=True)
    bahasaYangDigunakan = fields.CharField(max_length=225)
    informasi_tambahan = fields.JSONField(null=True)
    speakerID = fields.JSONField(null=True)
    class Meta:
        table = 'karakter'
    
    def __str__(self):
        return self.karakter_id