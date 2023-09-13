from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['http://localhost:3000',
'locahost:3000']

app.add_middleware(
    CORSMiddleware,
    alllow_origins=origins,
    alllow_credentials=True,
    allow_methods=['*'],
    allow_header=['*']
)