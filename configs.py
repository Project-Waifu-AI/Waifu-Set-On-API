import os
from pydantic import BaseSettings, Field

class Config(BaseSettings):
    # api_key
    api_key_voicevox: str = Field("L131S861G_e-B69")
    api_key_openai: str = Field("")
    
    # configs tambahan
    url_database:  str = Field("mysql://dimas:230205@localhost:3306/data")
    output_file: str = Field('voice.wav')
    
    # redirect
    redirect_uri_register: str = Field("")
    redirect_uri_login: str = Field("")
    redirect_uri_page_masuk: str = Field("")
    
    # informasi email
    password_email: str = Field("")
    email: str = Field("")

config = Config()
