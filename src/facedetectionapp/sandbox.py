"""Script used to test the web app.
"""  # noqa: E501

import requests
import base64
import cv2
import pickle
import codecs
import base64

path_to_img = "images_client/single_face.jpg"
with open(path_to_img, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
payload ={"filedata": encoded_string}

url = "http://localhost:5000/face_detect"
response = requests.post(url, data=payload)
result = response.json()
print("*"*30)
print("Test endpoint /face_detect")
print(result['face_detected'], result['message'])
print("*"*30)

print("*"*30)
print("Test endpoint /landmark_extraction")
url = "http://localhost:5000/landmark_extraction"
response = requests.post(url, data=payload)
result = response.json()
print(result['land_marks'], result['message'])
print("*"*30)

print("*"*30)
print("Test endpoint /crop_face")
url = "http://localhost:5000/crop_face"
response = requests.post(url, data=payload)
result = response.json()
print(result['message'])
if len(result['cropped_image']) > 0:
    obj_reconstituted = pickle.loads(codecs.decode(result['cropped_image'][0].encode('latin1'), "base64"))
    crop = obj_reconstituted
    cv2.imwrite("crop.jpg", crop)
print("*"*30)