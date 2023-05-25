import requests
from PIL import Image
import io
import base64


def count(image):
    # The URL of the endpoint
    url = "https://cellcounter.onrender.com/detect"
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    data = {
        'image': base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    }

    # Send the HTTP POST request and receive the response
    response = requests.post(url, json=data, timeout=240)

    if response.status_code == 200:

        data = response.json()

        # Get the Base64-encoded image data
        image_base64 = data['image']
        num = data['number']

        # image_data = response.content

        # Decode the Base64-encoded image data to bytes
        image_bytes = base64.b64decode(image_base64)

        # Open the image data as an Image object
        image = Image.open(io.BytesIO(image_bytes))


    else:
        print("It is ok ,All is Well", response.status_code)

    return image, num


def bnw(image, slider):
    # The URL of the endpoint
    # url = "http://127.0.0.1:8000/bnw"
    url = "https://cellcounter.onrender.com/bnw"
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    data = {
        'image': base64.b64encode(img_byte_arr.getvalue()).decode('utf-8'),
        'slider': slider
    }

    # Send the HTTP POST request and receive the response
    response = requests.post(url, json=data, timeout=240)

    if response.status_code == 200:

        data = response.json()

        # Get the Base64-encoded image data
        image_base64 = data['image']

        # image_data = response.content

        # Decode the Base64-encoded image data to bytes
        image_bytes = base64.b64decode(image_base64)
        image_byte = io.BytesIO(image_bytes)

        # Open the image data as an Image object
        image = Image.open(image_byte).convert('RGB')



    else:
        print("It is ok ,All is Well", response.status_code)

    return image
