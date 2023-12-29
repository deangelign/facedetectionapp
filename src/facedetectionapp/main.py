import uuid
import base64
import numpy as np
import cv2
import os
import json
import pickle
import codecs
from fastapi import FastAPI, File, Form
from datetime import datetime
from typing import List
from facedetectionapp.insightface_wrapper import FaceAnalyzer

app = FastAPI()
face_detector = FaceAnalyzer()

IMAGE_FODLER = 'uploaded_images/'
    
def _generate_filename(endpoint: str = "") -> str:
    dt = datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%s")
    random_name = str(uuid.uuid4())
    filename = os.path.join(IMAGE_FODLER, f"{dt}_{endpoint}_{random_name}.jpg" )
    return filename

def _save_image_bytes(encoded_string: str, filename: str):
    image_as_bytes = str.encode(encoded_string)  # convert string to bytes
    img_recovered = base64.b64decode(image_as_bytes)  # decode base64string
    with open(filename , "wb") as f:
        f.write(img_recovered)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/face_detect')
async def face_detect(filedata: str = File(...)) -> dict:
    """
    Detects if a face is present in the given image.

    Args:
        filedata (str): Base64-encoded string of the image.

    Returns:
        dict: A dictionary with the result indicating whether a face is detected.
    """
    contain_faces = False
    try:
        filename = _generate_filename("face_detect")
        _save_image_bytes(filedata, filename)
        img = cv2.imread(filename)
        if face_detector.detect_face(img):
            contain_faces = True
    except Exception as e:
        return {
            "face_detected": False,
            "message": f"Exception raised {e}"
        }
        
    return {
        "face_detected": contain_faces,
        "message": "Successfully uploaded image"
        } 

@app.post('/landmark_extraction')
async def landmark_extraction(filedata: str = File(...)) -> dict:
    """
    Extracts facial landmarks from the given image.

    Args:
        filedata (str): Base64-encoded string of the image.

    Returns:
        dict: A dictionary with the extracted landmarks.
    """
    try:
        filename = _generate_filename("landmark_extraction")
        _save_image_bytes(filedata, filename)
        img = cv2.imread(filename)
        land_marks = face_detector.extract_landmarks(img)
    except Exception as e:
        return {
            "land_marks": [],
            "message": f"Exception raised {e}"
        }
    
    land_marks
    return {
        "land_marks": land_marks,
        "message": f"Successfully uploaded image"
        }

@app.post('/crop_face')
async def crop_face(filedata: str = File(...)) -> dict:
    """
    Crops the face from the given image.

    Args:
        image_base64 (str): Base64-encoded string of the image.

    Returns:
        dict: A dictionary with the base64-encoded string of the cropped face image.
    """
    try:
        filename = _generate_filename("crop_face")
        _save_image_bytes(filedata, filename)
        img = cv2.imread(filename)
        cropped_face = face_detector.crop_face(img)
        if cropped_face is not None:
            obj_base64string = codecs.encode(pickle.dumps(cropped_face, protocol=pickle.HIGHEST_PROTOCOL), "base64").decode('latin1')
        else:
            obj_base64string = None
    except Exception as e:
        return {
            "cropped_image": [],
            "message": f"Exception raised {e}"
        }    
    return {
        "cropped_image": [obj_base64string] if obj_base64string is not None else [],
        "message": f"Successfully uploaded image"
    }