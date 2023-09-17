import os
from pydantic import BaseSettings, Field

class Config(BaseSettings):
    # api_key
    api_key_openai: str = Field("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")
    
    # configs tambahan
    url_database:  str = Field("mysql://root:123456@localhost:3306/data")
    output_file: str = Field('voice.wav')
    
    # redirect
    redirect_uri_register: str = Field("")
    redirect_uri_login: str = Field("")
    redirect_uri_page_masuk: str = Field("")
    
    # informasi email
    password_email: str = Field("zgqpdsundqzzzcbq")
    email: str = Field("dimas.ngadinegaran@gmail.com")

config = Config()
