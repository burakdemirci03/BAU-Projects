import os
from flask import Flask, request
from twilio.rest import Client
from dotenv import load_dotenv
from essential_functions import select_person
from adding_to_database import add_people

load_dotenv()

app = Flask(__name__)

account_sid = os.getenv("sid")
auth_token = os.getenv("token")
from_number = os.getenv("from_number")
to_number = select_person('bd')

client = Client(account_sid, auth_token)


@app.route("/incoming", methods=["POST"])
def incoming_message():
    user_msg = request.form.get("Body", "").strip().lower()

    if user_msg == "evet":
        e = client.messages.create(
        from_=f'whatsapp:{from_number}',
        body='Kapıyı açtınız.',
        to=f'whatsapp:{to_number}'
        )
        add_messg = client.messages.create(
        from_=f'whatsapp:{from_number}',
        content_sid=os.getenv("adding_people"),
        to=f'whatsapp:{to_number}'
        )

    elif user_msg in ["hayır", "açma"] :
        h = client.messages.create(
        from_=f'whatsapp:{from_number}',
        body='Kapıyı açmadınız.',
        to=f'whatsapp:{to_number}'
        )
        return 'OK', 200
    
    elif user_msg == "aç":
        e = client.messages.create(
        from_=f'whatsapp:{from_number}',
        body='Kapıyı açtınız.',
        to=f'whatsapp:{to_number}'
        )
        return 'OK', 200
    
    elif user_msg == "kaydet":
        k = client.messages.create(
        from_=f'whatsapp:{from_number}',
        body='Lütfen kaydedeceğiniz kişinin adını yazın.',
        to=f'whatsapp:{to_number}'
        )
        return 'OK', 200

    elif user_msg == "kaydetme":
        return 'OK', 200
    
    else:
        add_people(user_msg, to_number)
        return 'OK', 200


if __name__ == "__main__":
    app.run(port=8000, debug=True)
