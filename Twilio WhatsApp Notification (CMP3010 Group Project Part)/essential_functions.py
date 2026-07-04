import os
import re
import unicodedata
import requests
from dotenv import load_dotenv

load_dotenv()

imgbb_api_key = os.getenv("imgbb")

latest_image_path = os.path.join(os.path.dirname(os.getcwd()), 'detected_faces')
database_path = os.path.join(os.path.dirname(os.getcwd()), "photos")

people = list(zip(os.getenv("to_person").split(","), os.getenv("to_numbers").split(",")))


def select_person(name='bd'):
    for person, number in people:
        if name == person:
            return number
    raise ValueError(f"Kişi '{name}' listede bulunamadı.")

def get_last_image_path(im_path=latest_image_path):
    files = [
        os.path.join(im_path, f)
        for f in os.listdir(im_path)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def get_last_image_name(last_img_path=get_last_image_path()):
    last_img_name = os.path.basename(last_img_path)
    name, ext = os.path.splitext(last_img_name)
    return name, ext

def get_last_image(image_path=get_last_image_path()):
    with open(image_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": imgbb_api_key,
            }
        files = {
            "image": file,
            }
        response = requests.post(url, data=payload, files=files)
        
        if response.status_code == 200:
            return response.json()["data"]["url"]
        else:
            raise Exception(f"Fotoğraf yüklenemedi. Hata: {response.text}")
        
def is_people_known(name, db_path=database_path):
    files = os.listdir(db_path)
    people_set = set()
    for f in files:
        without_ext = os.path.splitext(f)[0]
        without_id = re.sub(r"\([a-zçğıöşü_]+\)$", "", without_ext, flags=re.IGNORECASE)
        normalized_name = unicodedata.normalize('NFC', without_id)
        people_set.add(normalized_name)
    name = re.sub(r"\([a-zçğıöşü_]+\)$", "", name, flags=re.IGNORECASE)
    name = unicodedata.normalize('NFC', name).lower()
    return name in people_set
