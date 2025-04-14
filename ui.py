import PySimpleGUI as sg
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

image_frame = sg.Frame(
    "Előnézet",
    [[sg.Image(filename="", size=(300, 300), key="-IMAGE-")]],
    size=(300, 300),
    relief=sg.RELIEF_SUNKEN, 
)

def kep_keszites():
    print("Kepkeszites elindult!")
    camera = Picamera2()
    camera.configure(camera.create_still_configuration())
    camera.start()

    image = camera.capture_array()
    image_path = "/home/danikaszman/Desktop/Images/image.jpg"
    cv2.imwrite(image_path, image)
    
    # Kép konvertálása megjeleníthető formába
    _, img_encoded = cv2.imencode('.png', image)
    img_bytes = img_encoded.tobytes()

    camera.stop() 
    camera.close()
    sleep(1)
    return image_path, img_bytes

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

    if felismert_szoveg:
        return felismert_szoveg
    else:
        window["-TEXT-"].update("Névfelismerés sikertelen!", text_color="red")

def datum_felismeres(image_path):
    print("Datumfelismeres elindult!")
    felismert_szoveg = pytesseract.image_to_string(Image.open(image_path))
    pattern = r"\b(\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}|\d{2}\.\d{2}\.\d{4})\b"
    felismert_datum = re.search(pattern, felismert_szoveg)

    if felismert_datum:
        return felismert_datum.group()  
    else:
        window["-TEXT-"].update("Dátumfelismerés sikertelen!", text_color="red")

def adatbazisba_mentes(felismert_nev, felismert_datum):
    print("Adatbazis feltoltes elindult!")
    uj_termek = {
        "NameOfProduct": felismert_nev,
        "ExpiryDate": felismert_datum,
    }

    products = collection.insert_one(uj_termek).inserted_id

# Define the layout of the GUI
layout = [
    [image_frame],
    [sg.Image(key='-IMAGE-')],
    [sg.Text('Termék neve:'), sg.InputText(readonly = True, key='-INPUT1-')],
    [sg.Text('Lejárati dátum:'), sg.InputText(readonly = True, key='-INPUT2-')],
    [sg.Button('Név fénykép', size=(15, 2), button_color=("white", "blue")), 
     sg.Button('Dátum fénykép', size=(15, 2), button_color=("white", "blue")), 
     sg.Push(), 
     sg.Button('Mentés', size=(10, 2), button_color=("white", "green"))],
    [sg.Text("", key="-TEXT-")],
]

# Create the window
window = sg.Window('Raspberry Pi Camera GUI', layout)

felismert_nev = ""
felismert_datum = ""

# Event loop
while True:
    event, values = window.read(timeout=100)
    
    if event == sg.WINDOW_CLOSED:
        break
    
    if event == 'Név fénykép':
        image_path, img_bytes = kep_keszites()
        window['-IMAGE-'].update(data=img_bytes)

        kepfeldolgozas(image_path)
        felismert_nev = szoveg_felismeres(image_path)
        
        window['-INPUT1-'].update(felismert_nev)
    
    if event == 'Dátum fénykép':
        image_path, img_bytes = kep_keszites()
        window['-IMAGE-'].update(data=img_bytes)

        kepfeldolgozas(image_path)
        felismert_datum = datum_felismeres(image_path)

        window['-INPUT2-'].update(felismert_datum)

    if event == 'Mentés':
        if felismert_nev or felismert_datum:
            adatbazisba_mentes(felismert_nev, felismert_datum)
        else:
            window["-TEXT-"].update("Név vagy dátum hiányzik!", text_color="red")

        
        window['-INPUT1-'].update("")    
        window['-INPUT2-'].update("")
        felismert_nev = ""
        felismert_datum = ""
        window["-TEXT-"].update("Sikeresen mentve az adatbázisba!", text_color="green")

window.close()
