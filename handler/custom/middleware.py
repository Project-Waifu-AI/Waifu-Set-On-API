# custom_middleware.py
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi.exceptions import HTTPException

async def custom_exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as exc:
        # Handle HTTPException
        detail = exc.detail
        if isinstance(detail, dict):
            content = {key: value for key, value in detail.items()}
        
        return JSONResponse(status_code=exc.status_code, content=content)
