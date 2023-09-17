from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import init_db
from configs import config
import api.BecomWaifu 
import autentikasi.google_auth
import autentikasi.wso_auth
import api.AsistenWaifu
import openai

app = FastAPI()
openai.api_key = config.api_key_openai

@app.on_event("startup")
async def startup():
    init_db(app)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api.BecomWaifu.router)
app.include_router(autentikasi.google_auth.router)
app.include_router(autentikasi.wso_auth.router)
app.include_router(api.AsistenWaifu.router)