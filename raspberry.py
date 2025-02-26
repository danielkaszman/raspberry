import io
import os
import cv2
import re
import pymongo
import pytesseract
import libcamera
from PIL import Image
from picamera2 import Picamera2
from time import sleep
#from google.cloud import vision
from datetime import datetime

# Google hitelesítési kulcs (JSON fájl)
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "raspberry/fridge-key.json"


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

# MongoDB kapcsolat
client = pymongo.MongoClient("mongodb+srv://danikaszman:danikaszman@cluster.soqfcau.mongodb.net/Products?retryWrites=true&w=majority&appName=Cluster")
db = client["Products"]
collection = db["products"]

def kep_keszites():
    print("Kepkeszites elindult!")
    camera = Picamera2()
    camera.configure(camera.create_still_configuration())
    camera.start()

    image = camera.capture_array() 
    image_path = "/home/danikaszman/Desktop/Images/image.jpg"
    cv2.imwrite(image_path, image)
        
    camera.stop()
    return image_path

def kepfeldolgozas(image_path):
    image = cv2.imread(image_path)    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    denoised = cv2.fastNlMeansDenoising(
            gray_image, 
            h = 260,      # Adjust based on noise level (higher = stronger denoising)
            templateWindowSize=7, 
            searchWindowSize=21
        )
    return denoised
    
def szoveg_felismeres(denoised):
    print("Szovegfelismeres elindult!")
    felismert_szoveg = pytesseract.image_to_string(Image.open(denoised))
    return felismert_szoveg

def adatbazisba_mentes():
    uj_termek = {
        "nev": "Tej",
        "lejarat": "2025-03-10",
    }

    inserted_id = collection.insert_one(uj_termek).inserted_id

def main():
    print("Main elindult!")
    image_path = kep_keszites()
    denoised = kepfeldolgozas(image_path)
    felismert_szoveg = szoveg_felismeres(denoised)
    #text = detect_text(image_path)
    #expiration_date = extract_expiration_date(text)
    #save_to_mongodb(text, expiration_date)
    print(f"Felismert termék: {felismert_szoveg}")

if __name__ == "__main__":
    main()
