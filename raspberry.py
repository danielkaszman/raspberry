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
from datetime import datetime

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
    print("Kepfeldolgozas elindult!")
    image = cv2.imread(image_path)    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    denoised = cv2.fastNlMeansDenoising(
            gray_image, 
            h = 260,      
            templateWindowSize=7, 
            searchWindowSize=21
        )

    cv2.imwrite(image_path, denoised)
    return 
    
def szoveg_felismeres(image_path):
    print("Szovegfelismeres elindult!")
    felismert_szoveg = pytesseract.image_to_string(Image.open(image_path))
    return felismert_szoveg

def datum_felismeres(image_path):
    print("Datumfelismeres elindult!")
    felismert_szoveg = pytesseract.image_to_string(Image.open(image_path))
    pattern = r"\b(\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}|\d{2}\.\d{2}\.\d{4})\b"
    felismert_datum = re.search(pattern, felismert_szoveg)
    if felismert_datum:
        return felismert_datum.group()  
    else:
        return None  

def adatbazisba_mentes(datum):
    print("Adatbazis feltoltes elindult!")
    uj_termek = {
        "NameOfProduct": "Teszt termék",
        "ExpiryDate": datum,
    }

    products = collection.insert_one(uj_termek).inserted_id

def main():
    print("Main elindult!")
    image_path = kep_keszites()
    kepfeldolgozas(image_path)
    felismert_szoveg = szoveg_felismeres(image_path)
    felismert_datum = datum_felismeres(image_path)

    print(f"Felismert szoveg: {felismert_szoveg}")
    print(f"Felismert datum: {felismert_datum}")

    if felismert_datum:
        adatbazisba_mentes(felismert_datum)
        

if __name__ == "__main__":
    main()
