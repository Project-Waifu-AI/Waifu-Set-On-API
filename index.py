from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import init_db
from configs import config
from api.router import router

import openai

app = FastAPI()
openai.api_key = config.api_key_openai

@app.on_event("startup")
async def startup():
    init_db(app)

origins = [
    "http://localhost:3000",
    "localhost:3000",
    'https://9ec8-103-105-55-169.ngrok-free.app'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router=router)