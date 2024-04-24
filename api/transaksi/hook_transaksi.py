from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from helper.cek_and_set import cek_data_user
from helper.premium import create_token_premium
from database.model import anonimBuyer

router = APIRouter(prefix='/transaksi', tags=['pembayaran-wso'])

@router.post('/planning-socilabuz')
async def plan_socialbuz(req: Request):
    try:
        data = await req.json()
        print(data)
        id_pembayaran = data.get('id')
        email = data.get('buyer_email') or 'anonim'
        nama = data.get('buyer_name') or 'anonim'
        no_telp = data.get('buyer_whatsapp') or '---'
        jumlah_dibayar = data.get('price')
        currency = data.get('currency')
        product = data.get('title')

        if cek_data_user(email) is False:
            try:
                await anonimBuyer.save(id_pembayaran=id_pembayaran, email=email, nama=nama, no_telp=no_telp, jumlah_dibayar=jumlah_dibayar, currency=currency, object_buy=product)
            except Exception as e:
                raise HTTPException(status_code=500, detail=e)
        
        create_premium_data = await create_token_premium(email=email, plan=product)
        if create_premium_data['status'] is False:
            raise HTTPException(detail=create_premium_data['keterangan'], status_code=500)
        
        return JSONResponse ({'message': 'Webhook received successfully'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

# socialbuz shop struct json webhook request
'''
{"id":8645410,"amount":10000,"currency":"IDR","amount_settled":10000,
"currency_settled":"IDR","buyer_name":"Jessica","buyer_email":"jessica@example.com",
"buyer_whatsapp":"","item_id":1,"title":"Produk","price":10000,
"link":"https://sociabuzz.com/shop","created_at":"2024-04-20T13:13:52+07:00"}
'''

@router.post('/support-socialbuz')
async def support_socialbuz(req: Request):
    try:
        data = await req.json()
        print(data.get('email_supporter'))
        return {'message': 'Webhook received successfully'}
    except Exception as e:
        print(f"Error processing request: {e}")
        return {'message': 'Error processing webhook request'}

#socialbuz stribe struct json webhook request
'''
b'{"id":"2409329842","amount":10000,"currency":"IDR",
"amount_settled":10000,"currency_settled":"IDR",
"media_type":"","media_url":"","supporter":"Jessica",
"email_supporter":"jessica@example.com",
"message":"Ini hanya test notifikasi",
"created_at":"2024-04-23T16:49:09+07:00"}'
'''

@router.post('/planning-saweria')
async def plan_saweria(req: Request):
    try:
        data = await req.json()
        print(data)
        return {'message': 'Webhook received successfully'}
    except Exception as e:
        print(f"Error processing request: {e}")
        return {'message': 'Error processing webhook request'}    

# saweria struct json webhook request
'''
{"version": "2022.01", "created_at": "2021-01-01T12:00:00+00:00", 
"id": "00000000-0000-0000-0000-000000000000", "type": "donation", 
"amount_raw": 69420, "cut": 3471, "donator_name": "Someguy", 
"donator_email": "someguy@example.com", "donator_is_user": false, 
"message": "THIS IS A FAKE MESSAGE! HAVE A GOOD ONE"}
'''