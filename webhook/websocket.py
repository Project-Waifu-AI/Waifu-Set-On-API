from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import JSONResponse
from pydub import AudioSegment
import os

'''
app = APIRouter(prefix='/websocket', tags=['websocket'])


async def proses_audio(data: WebSocket):
    

@app.websocket('/audio-proses')
async def audio_realtime(websocket: WebSocket):
    await websocket.accept()
    
    try:
        await 

'''