"""Script used to test the web app.
"""  # noqa: E501

import base64
import codecs
import pickle
import cv2
import requests  # type: ignore


def _landmark_get_color_rgb(index):
    if 0 <= index <= 32:
        return [255, 0, 0]  # Red for color1
    elif 33 <= index <= 42:
        return [0, 255, 0]  # Green for color2
    elif 43 <= index <= 51:
        return [0, 0, 255]  # Blue for color3
    elif 52 <= index <= 71:
        return [255, 255, 0]  # Yellow for color4
    elif 72 <= index <= 86:
        return [255, 0, 255]  # Magenta for color5
    elif 87 <= index <= 96:
        return [0, 255, 255]  # Cyan for color6
    elif 97 <= index <= 105:
        return [128, 128, 128]  # Gray for color7
    else:
        return [0, 0, 0]  # Default color


def _draw_landmarks(image, landmarks):
    image_cp = image.copy()

    for row, point in enumerate(landmarks):
        x, y = point
        x, y = int(x), int(y)
        color = _landmark_get_color_rgb(row)  # RGB
        color.reverse()  # BGR
        cv2.circle(image_cp, (x, y), 1, color, 2)
    return image_cp


path_to_img = "images_client/single_face.jpg"
img = cv2.imread(path_to_img)
with open(path_to_img, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
payload = {"filedata": encoded_string}

url = "http://localhost:5000/face_detect"
response = requests.post(url, data=payload)
result = response.json()
print("*" * 30)
print("Test endpoint /face_detect")
print(result["face_detected"], result["message"])
print("*" * 30)

print("*" * 30)
print("Test endpoint /landmark_extraction")
url = "http://localhost:5000/landmark_extraction"
response = requests.post(url, data=payload)
result = response.json()
landmarks = result["land_marks"]
img_l = _draw_landmarks(img, landmarks)
cv2.imwrite("landmarks.jpg", img_l)
print(landmarks, result["message"])

print("*" * 30)

print("*" * 30)
print("Test endpoint /crop_face")
url = "http://localhost:5000/crop_face"
response = requests.post(url, data=payload)
result = response.json()
print(result["message"])
if len(result["cropped_image"]) > 0:
    obj_reconstituted = pickle.loads(
        codecs.decode(result["cropped_image"][0].encode("latin1"), "base64")
    )
    crop = obj_reconstituted
    cv2.imwrite("crop.jpg", crop)
print("*" * 30)
