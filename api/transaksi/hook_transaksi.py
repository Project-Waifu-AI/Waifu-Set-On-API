from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from helper.cek_and_set import cek_data_user, cek_hookID
from helper.premium import create_token_premium
from database.model import anonim_buyer, hall_of_support

router = APIRouter(prefix='/transaksi', tags=['pembayaran-wso'])

@router.post('/planning-socilabuz/{id}')
async def plan_socialbuz(id: str, req: Request):
    try:
        if await cek_hookID(id=id) is False:
            raise HTTPException(detail='invalid hook parameter', status_code=404)
        
        data = await req.json()
        print(data)
        
        user_data = await cek_data_user(data.get('buyer_email'))
        if not user_data:
            
            save = anonim_buyer(
                id_transaksi = str(data.get('id')),
                service = 'socialbuz',
                email = data.get('buyer_email') or 'anonim',
                nama = data.get('buyer_name') or 'anonim',
                no_telp = data.get('buyer_whatsapp') or '---',
                object_buy = data.get('title'),
                nominal = int(data.get('price')),
                currency = data.get('currency'),
                waktu = data.get('created_at')
            )
            
            await save.save()
        else:
            create_premium_data = await create_token_premium(email=data.get('buyer_email'), plan=data.get('title'))
            if create_premium_data['status'] is False:
                raise HTTPException(detail=create_premium_data['keterangan'], status_code=500)

        return JSONResponse({'message': 'Webhook received successfully'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/support-socialbuz/{id}')
async def support_socialbuz(id: str, req: Request):
    
    try:
        if await cek_hookID(id=id) is False:
            raise HTTPException(detail='invalid hook parameter', status_code=404)
        
        data = await req.json()
        print(data)

        save = hall_of_support(
            id_transaksi = data.get('id'),
            service = 'socialbuz',
            email = data.get('email_supporter'),
            nama = data.get('supporter'),
            pesan = data.get('message'),
            nominal = data.get('amount_settled'),
            currency = data.get( 'currency_settled'),
            waktu = data.get('created_at')
        )
        await save.save()

        return {'message': 'Webhook received successfully'}
    except Exception as e:
        print(f"Error processing request: {e}")
        return {'message': 'Error processing webhook request'}

@router.post('/support-saweria/{id}')
async def plan_saweria(id: str, req: Request):
    try:
        if await cek_hookID(id=id) is False:
            raise HTTPException(detail='invalid hook parameter', status_code=404)
        
        data = await req.json()
        print(data)
        
        save = hall_of_support(
            id_transaksi = data.get('id'),
            service = 'saweria',
            email = data.get('donator_email'),
            nama = data.get('donator_name'),
            pesan = data.get('message'),
            nominal = data.get('amount_raw'),
            currency = 'IDR',
            waktu = data.get('created_at')
        )
        await save.save()

        return {'message': 'Webhook received successfully'}
    except Exception as e:
        print(f"Error processing request: {e}")
        return {'message': 'Error processing webhook request'}