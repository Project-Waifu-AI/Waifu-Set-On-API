from fastapi import APIRouter, Request

router = APIRouter(prefix='/pembayaran', tags=['pembayaran-wso'])

@router.post('/notification')
def notif(req: Request):
    print(str(req))


@router.get('/notification')
def notif(req: Request):
    print(str(req))