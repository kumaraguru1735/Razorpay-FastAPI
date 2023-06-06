from fastapi import FastAPI
from fastapi.responses import JSONResponse
import razorpay
from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()
razorpay_key_id = os.getenv("RAZORPAY_KEY_ID")
razorpay_key_secret = os.getenv("RAZORPAY_KEY_SECRET")


class CreateOrder(BaseModel):
    amount: int
    currency: str = "INR"

class VerifyOrder(BaseModel):
    order_id: str

class DeleteOrder(BaseModel):
    order_id: str

app = FastAPI()
client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/create_order")
def create_order(input: CreateOrder):
    payment = client.order.create({'amount': input.amount, 'currency': input.currency, 'payment_capture': '1'})
    print(payment)
    return payment

@app.post("/verify_order")
async def verify_order(input: VerifyOrder):
    try:
        order = client.order.fetch(input.order_id)

        if order['status'] == 'paid':
            # Payment successful, update your database or do other tasks here
            return JSONResponse(status_code=200, content={'message': 'Payment successfull'})
        else:
            # Payment failed, handle the failure here
            return JSONResponse(status_code=500, content={'message': 'Payment failed'})
    except Exception as e:
        # Handle any exceptions here
        return JSONResponse(status_code=500, content={'message': str(e)})
    

@app.post("/delete_order")
async def delete_order(input: DeleteOrder):
    try:
        order = client.order.fetch(input.order_id)
        if order['status'] == 'created':
            client.order.delete(input.order_id)
            return JSONResponse(status_code=200, content={'message': 'Order deleted'})
        else:
            return JSONResponse(status_code=400, content={'message': 'Order cannot be deleted'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': str(e)})