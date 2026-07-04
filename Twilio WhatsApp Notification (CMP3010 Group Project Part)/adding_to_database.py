import os
import re
from twilio.rest import Client
from dotenv import load_dotenv
from essential_functions import get_last_image_path, get_last_image_name

load_dotenv()

account_sid = os.getenv("sid")
auth_token = os.getenv("token")
from_number = os.getenv("from_number")

client = Client(account_sid, auth_token)

last_img_path = get_last_image_path()
latest_path = os.path.dirname(last_img_path)
database_path = os.path.join(os.path.dirname(latest_path), "photos")

last_img_name, ext = get_last_image_name(last_img_path)


def create_folder(name, db_path=database_path):
    files = os.listdir(db_path)
    people_list = [f for f in files]

    if name not in people_list:
        os.makedirs(os.path.join(db_path, name))
        path = os.path.join(db_path, name)
        return path
    
    else:
        cnt = 1
        while True:
            person_folder = f"{name}_({cnt})"
            cnt += 1
            if person_folder not in people_list:
                os.makedirs(os.path.join(db_path, person_folder))
                path = os.path.join(db_path, person_folder)
                return path

def add_people(name, user_number):
    valid_name = re.match(r"^[a-zA-ZÇşŞğĞüÜöÖıİ\s?]+$", name)
    if not valid_name:
        k = client.messages.create(
        from_=f'whatsapp:{from_number}',
        body='Geçerli bir isim değil, lütfen yeniden deneyin.',
        to=f'whatsapp:{user_number}'
        )

    else:
        try:
            person_name = re.sub(r"\s+", "_", name).strip("_").lower()
            person_folder = create_folder(person_name)
            new_person_path = os.path.join(person_folder, person_name + ext)
            os.rename(last_img_path, new_person_path)

            k = client.messages.create(
                from_=f'whatsapp:{from_number}',
                body=f'{person_name.upper()} başarıyla kaydedildi.',
                to=f'whatsapp:{user_number}'
                )

        except Exception as e:
            k = client.messages.create(
                from_=f'whatsapp:{from_number}',
                body=f'Bir hata oluştu: {str(e)}',
                to=f'whatsapp:{user_number}'
                )
            