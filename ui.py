import PySimpleGUI as sg
import io
import time
from picamera2 import Picamera2
from PIL import Image

# Function to capture an image from the Raspberry Pi camera
def capture_image(camera):
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    image = Image.open(stream)
    return image

# Function to convert the image to a format suitable for PySimpleGUI
def convert_image_to_bytes(image):
    with io.BytesIO() as output:
        image.save(output, format='PNG')
        return output.getvalue()

# Initialize the camera
camera = Picamera2()

# Define the layout of the GUI
layout = [
    [sg.Image(key='-IMAGE-')],
    [sg.Text('Termek neve'), sg.InputText(key='-INPUT1-')],
    [sg.Text('Lejarati datum'), sg.InputText(key='-INPUT2-')],
    [sg.Button('Modify Input 1'), sg.Button('Modify Input 2')]
]

# Create the window
window = sg.Window('Raspberry Pi Camera GUI', layout)

# Capture the initial image
#image = capture_image(camera)
#image_bytes = convert_image_to_bytes(image)
#window['-IMAGE-'].update(data=image_bytes)

# Event loop
while True:
    event, values = window.read(timeout=100)
    
    if event == sg.WINDOW_CLOSED:
        break
    
    if event == 'Modify Input 1':
        # Modify input 1 (for example, append " modified" to the input)
        values['-INPUT1-'] += " modified"
        window['-INPUT1-'].update(values['-INPUT1-'])
    
    if event == 'Modify Input 2':
        # Modify input 2 (for example, append " modified" to the input)
        values['-INPUT2-'] += " modified"
        window['-INPUT2-'].update(values['-INPUT2-'])
    
    # Capture a new image every second
    #if time.time() % 1 < 0.1:  # Capture every second
     #   image = capture_image(camera)
      #  image_bytes = convert_image_to_bytes(image)
       # window['-IMAGE-'].update(data=image_bytes)

# Cleanup
camera.close()
window.close()
