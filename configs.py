import os
from typing import List
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    #admin
    admin = os.getenv('ADMIN')
    
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
    
    # redirect
    redirect_uri_register: str = Field("REDIRECT_URI_REGISTER")
    redirect_uri_login: str = Field("REDIRECT_URI_LOGIN")
    redirect_uri_page_masuk: str = Field("LINK_PAGE_MASUK")
    
    # informasi email
    email: str = os.getenv("EMAIL")
    password_email: str = os.getenv("PASSWORD_EMAIL")

    # JWT
    algoritma: str = os.getenv('ALGORITMA')
    secret_key: str = os.getenv('SECRET_KEY')

config = Config()
