import os
import asyncio
from dotenv import load_dotenv
from twilio.rest import Client
from essential_functions import select_person, get_last_image, get_last_image_name, is_people_known

load_dotenv()

account_sid = os.getenv("sid")
auth_token = os.getenv("token")
from_number = os.getenv("from_number")
to_number = select_person('bd')

client = Client(account_sid, auth_token)

last_img = get_last_image()
last_img_name = get_last_image_name()[0]


async def send_messages():
    image = client.messages.create(
        from_=f'whatsapp:{from_number}',
        media_url=[last_img],
        to=f'whatsapp:{to_number}'
        )
    
    await asyncio.sleep(3)

    if not is_people_known(last_img_name):
        notification = client.messages.create(
            from_=f'whatsapp:{from_number}',
            content_sid=os.getenv("unknown_people"),
            to=f'whatsapp:{to_number}'
            )
    
    else:
        notification = client.messages.create(
            from_=f'whatsapp:{from_number}',
            content_sid=os.getenv("known_people"),
            content_variables='{"1": "' + last_img_name.replace('_', ' ').upper() + '"}',
            to=f'whatsapp:{to_number}'
            )
        
            
if __name__ == "__main__":
    try:
        asyncio.run(send_messages())
    except Exception as e:
        print(f"Hata: {e}")
