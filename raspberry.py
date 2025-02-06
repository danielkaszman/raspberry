import io
import os
import cv2
import re
import pymongo
import pytesseract
from PIL import Image
from picamera import PiCamera
from time import sleep
from google.cloud import vision
from datetime import datetime

#Pi camera elindítása (lehet hogy a mainbe kell tenni)
camera = PiCamera()
camera.start_preview()

# Google hitelesítési kulcs (JSON fájl)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "raspberry/fridge-key.json"

# MongoDB kapcsolat
"""
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["product_database"]
collection = db["products"]
"""
#Ezek itt faszsagok
"""
def detect_text(image_path):
    client = vision.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    return ""
"""

"""
def extract_expiration_date(text):
    pattern = r"\b(\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}|\d{2}\.\d{2}\.\d{4})\b"
    match = re.search(pattern, text)
    return match.group(0) if match else "Nincs dátum"
"""

"""
def save_to_mongodb(product_name, expiration_date):
    data = {
        "product_name": product_name,
        "expiration_date": expiration_date,
        "timestamp": datetime.now()
    }
    collection.insert_one(data)
    print("Adat elmentve MongoDB-be.")
"""

def kep_keszites():
    image_path = '/home/pi/Desktop/image.jpg'
    camera.capture(image_path)
    sleep(1)
    return image_path
    
def szoveg_felismeres(image_path):
    felismert_szoveg = pytesseract.image_to_string(Image.open(image_path))
    return felismert_szoveg

def main():
    image_path = kep_keszites()
    felismert_szoveg = szoveg_felismeres(image_path)
    #text = detect_text(image_path)
    #expiration_date = extract_expiration_date(text)
    #save_to_mongodb(text, expiration_date)
    print(f"Felismert termék: {felismert_szoveg}")

if __name__ == "__main__":
    main()
