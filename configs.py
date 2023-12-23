import os
from typing import List
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    # redirect autentikasi
    redirect_uri_page_masuk: str = os.getenv('REDIRECT_PAGE_MASUK')
    redirect_uri_home: str = os.getenv('REDIRECT_HOME')
    
    # admin
    admin = os.getenv('ADMIN')
    
    # twiter
    client_id_twiter: str = os.getenv('CLIENT_ID_TWITER')
    client_secret_twiter: str = os.getenv('CLIENT_SECRET_TWITER')
    redirect_uri_autentikasi_twiter: str = os.getenv('REDIRECT_URI_AUTENTIKASI_TWITER')
    consumer_key_twiter: str = os.getenv('API_KEY_TWITER')
    consumer_secret_twiter: str = os.getenv('API_KEY_SECRET_TWITTER')
    access_token_twiter: str = os.getenv('ACCESS_TOKEN_TWITER')
    access_token_secret_twiter: str = os.getenv('ACCESS_TOKEN_SECRET_TWITER')
    
    # data
    bahasa={
        'bahasa indonesia': 'id',
        'English': 'en',
        '日本語': 'ja',
        'basa jawa': 'jv',
        'русский язык': 'ru',
        '한국어': 'ko'
    }
    
    # api_key_opneai
    api_key_openai: str = os.getenv("API_KEY_OPENAI")
    
    # configs tambahan
    url_database:  str = os.getenv("URL_DATABASE")
    output_file: str = Field('voice.wav')
    
    # redirect google
    redirect_uri_autentikasi_google: str = Field("REDIRECT_URI_AUTENTIKASI_GOOGLE")
    redirect_root_google: str = Field("http://waifuseton.wso:8000/api/auth/google/root")

    # domain smd
    smd_domain: str = os.getenv('API_SMD_DOMAIN_AUTH')
    
    # informasi email
    email: str = os.getenv("EMAIL")
    password_email: str = os.getenv("PASSWORD_EMAIL")

    # JWT
    algoritma: str = os.getenv('ALGORITMA')
    secret_key: str = os.getenv('SECRET_KEY')

config = Config()
