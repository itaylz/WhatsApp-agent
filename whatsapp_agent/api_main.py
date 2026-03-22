from fastapi import FastAPI, Request, Form
from twilio.twiml.messaging_response import MessagingResponse
import agent_brain # We will build this next

app = FastAPI()

@app.post("/whatsapp")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    # 1. Receive the message from WhatsApp
    user_message = Body
    sender = From

    # 2. Send the message to your AI logic
    ai_response = agent_brain.process_message(user_message)

    # 3. Format the response for Twilio to send back to WhatsApp
    twilio_resp = MessagingResponse()
    twilio_resp.message(ai_response)
    
    return str(twilio_resp)