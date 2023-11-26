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
    redirect_uri_login_twiter: str = os.getenv('REDIRECT_URI_LOGIN_TWITER')
    redirect_uri_register_twiter: str = os.getenv('REDIRECT_URI_REGISTER_TWITER')
    consumer_key_twiter: str = os.getenv('API_KEY_TWITER')
    consumer_secret_twiter: str = os.getenv('API_KEY_SECRET_TWITTER')
    access_token_twiter: str = os.getenv('ACCESS_TOKEN_TWITER')
    access_token_secret_twiter: str = os.getenv('ACCESS_TOKEN_SECRET_TWITER')
    
    # data
    bahasa={
        'bahasa indonesia': 'id-ID',
        'English': 'en-IN',
        '日本語': 'ja-JP',
        'basa jawa': 'jv-ID',
        'русский язык': 'ru-RU',
        '한국어': 'ko-KR'
    }
    
    # api_key
    api_key_openai: str = os.getenv("API_KEY_OPENAI")
    
    # configs tambahan
    url_database:  str = os.getenv("URL_DATABASE")
    output_file: str = Field('voice.wav')
    
    # redirect google
    redirect_uri_register_google: str = Field("REDIRECT_URI_REGISTER_GOOGLE")
    redirect_uri_login_google: str = Field("REDIRECT_URI_LOGIN_GOOGLE")
    redirect_uri_page_masuk_google: str = Field("LINK_PAGE_MASUK_GOOGLE")
    
    # informasi email
    email: str = os.getenv("EMAIL")
    password_email: str = os.getenv("PASSWORD_EMAIL")

    # JWT
    algoritma: str = os.getenv('ALGORITMA')
    secret_key: str = os.getenv('SECRET_KEY')

config = Config()
