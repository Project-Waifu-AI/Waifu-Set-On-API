from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database.database import init_db
from configs import config
from api.router import router
from handler.custom.middleware import custom_exception_middleware
import handler.database.signal

app = FastAPI()

@app.on_event("startup")
async def startup():
    init_db(app)

app.add_middleware(custom_exception_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router=router)