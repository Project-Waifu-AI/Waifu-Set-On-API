from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import init_db
from configs import config
import api.BecomWaifu 
import autentikasi.google_auth
import autentikasi.wso_auth
import autentikasi.user_set
import autentikasi.premium_auth
import api.AsistenWaifu
import api.admin_access
import api.gachapon
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

app.include_router(autentikasi.premium_auth.router)
app.include_router(api.BecomWaifu.router)
app.include_router(api.AsistenWaifu.router)
app.include_router(api.gachapon.router)
app.include_router(api.admin_access.router)
app.include_router(autentikasi.google_auth.router)
app.include_router(autentikasi.wso_auth.router)
app.include_router(autentikasi.user_set.router)