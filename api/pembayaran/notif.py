from fastapi import APIRouter, Request

router = APIRouter(prefix='/pembayaran', tags=['pembayaran-wso'])

@router.get('/notification')
def notif(req: Request):
    print(str(req))