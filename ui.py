import PySimpleGUI as sg
import io
import time
import libcamera
from picamera2 import Picamera2
from PIL import Image

image_frame = sg.Frame(
    "Előnézet",
    [[sg.Image(filename="", size=(200, 200), key="-IMAGE-")]],
    size=(500, 500),
    relief=sg.RELIEF_SUNKEN,  # Süllyesztett keret hatás
)

# Inicializáljuk a Picamera2-t
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)
picam2.start()

# Define the layout of the GUI
layout = [
    [image_frame],
    [sg.Image(key='-IMAGE-')],
    [sg.Text('Termék neve:'), sg.InputText(readonly = True, key='-INPUT1-')],
    [sg.Text('Lejárati dátum:'), sg.InputText(readonly = True, key='-INPUT2-')],
    [sg.Button('Fényképezés', size=(15, 2), button_color=("white", "blue")), sg.Push(), sg.Button('Mentés', size=(10, 2), button_color=("white", "green"))],
    
]

# Create the window
window = sg.Window('Raspberry Pi Camera GUI', layout)

# Event loop
while True:
    event, values = window.read(timeout=100)
    
    if event == sg.WINDOW_CLOSED:
        break

    # Kép rögzítése
    array = picam2.capture_array()
    #array = np.rot90(array)  # Forgatás, ha szükséges
    #array = np.flipud(array)  # Tükrözés, ha szükséges

    # Kép konvertálása PySimpleGUI számára
    img_bytes = array.tobytes()
    window['-IMAGE-'].update(data=img_bytes, size=(500, 500))
    
    if event == 'Fényképezés':
        values['-INPUT1-'] += " modified"
        window['-INPUT1-'].update(values['-INPUT1-'])
    
    if event == 'Mentés':
        values['-INPUT2-'] += " modified"
        window['-INPUT2-'].update(values['-INPUT2-'])

window.close()
