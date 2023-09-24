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
    output = fields.CharField(max_length=225)
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
    ulang_tahun = fields.DateField(null=True)
    gender = fields.CharField(max_length=10, null=True)
    email = fields.CharField(max_length=225)
    password = fields.BinaryField(max_length=225,null=True)
    NegaiKanjo = fields.IntField(null=True)
    karakter = fields.JSONField()
    akunwso = fields.BooleanField(default=False)
    token_konfirmasi = fields.CharField(max_length=225, null=True)
    status = fields.BooleanField(default=False)
    ban = fields.BooleanField(default=False)

    class Meta:
        table = "userdata"

    def __str__(self):
        return self.user_id

class premium(Model):
    user_id = fields.CharField(max_length=225, pk=True)
    premium = fields.BooleanField(default=False)
    waktu_basi = fields.DatetimeField(null=True)
    
    class Meta:
        table = 'premium'
    
    def __str__(self):
        return self.user_id

class KarakterData(Model):
    karakter_id = fields.IntField(pk=True)
    nama = fields.CharField(max_length=225)
    kepribadian = fields.CharField(max_length=225)
    usia = fields.IntField(null=True)
    ulang_tahun = fields.DateField(null=True)
    model_suara = fields.BinaryField(null=True)
    class Meta:
        table = 'karakter'
    
    def __str__(self):
        return self.karakter_id

class access_token_data(Model):
    access_token = fields.UUIDField(pk=True)
    waktu_basi = fields.DatetimeField()
    user_id = fields.CharField(max_length=225)
    
    class Meta:
        table = "access_token"
        
    def __str__(self):
        return self.access_token