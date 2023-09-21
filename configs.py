import os
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    # api_key
    api_key_openai: str = os.getenv("API_KEY_OPENAI")
    
    # configs tambahan
    url_database:  str = os.getenv("URL_DATABASE")
    output_file: str = Field('voice.wav')
    
    # redirect
    redirect_uri_register: str = Field("")
    redirect_uri_login: str = Field("")
    redirect_uri_page_masuk: str = Field("")
    
    # informasi email
    email: str = os.getenv("EMAIL")
    password_email: str = os.getenv("PASSWORD_EMAIL")

config = Config()
