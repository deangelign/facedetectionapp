import unittest
import base64
import pickle
import codecs
import cv2
from facedetectionapp.main import app
from fastapi.testclient import TestClient

class TestEndpointsFaceDetect(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        
        path_to_img = "images_client/single_face.jpg"
        with open(path_to_img, "rb") as image_file:
            self.encoded_string_face = base64.b64encode(image_file.read())

        path_to_img = "images_client/no_face.jpg"
        with open(path_to_img, "rb") as image_file:
            self.encoded_string_no_face = base64.b64encode(image_file.read())

        self.payload = {"filedata": None}
        self.sucess_upload_msg = "Successfully uploaded image"
        
    def test_face_detect_face_true(self):
        self.payload['filedata'] = self.encoded_string_face
        response = self.client.post('/face_detect', data=self.payload)
        result = response.json()
        self.assertIn('face_detected', result)
        self.assertIn('message', result)
        self.assertEqual(result['face_detected'], True)
        self.assertEqual(result['message'], self.sucess_upload_msg)

    def test_face_detect_face_false(self):
        self.payload['filedata'] = self.encoded_string_no_face
        response = self.client.post('/face_detect', data=self.payload)
        result = response.json()
        self.assertIn('face_detected', result)
        self.assertIn('message', result)
        self.assertEqual(result['face_detected'], False)
        self.assertEqual(result['message'], self.sucess_upload_msg)

    def test_face_detect_exception_no_bytes(self):
        self.payload['filedata'] = self.encoded_string_no_face
        response = self.client.post('/face_detect', data="")
        result = response.json()
        self.assertNotIn('face_detected', result)
        self.assertNotIn('message', result)

    def test_face_detect_exception_incorrect_bytes(self):
        self.payload['filedata'] = self.encoded_string_face[0:10]
        response = self.client.post('/face_detect', data=self.payload)
        result = response.json()
        self.assertIn('face_detected', result)
        self.assertIn('message', result)
        self.assertEqual(result['face_detected'], False)
        self.assertEqual(result['message'], 'Exception raised Incorrect padding')

class TestEndpointsLandmarkExtraction(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        
        path_to_img = "images_client/single_face.jpg"
        with open(path_to_img, "rb") as image_file:
            self.encoded_string_face = base64.b64encode(image_file.read())

        path_to_img = "images_client/no_face.jpg"
        with open(path_to_img, "rb") as image_file:
            self.encoded_string_no_face = base64.b64encode(image_file.read())

        self.payload = {"filedata": None}
        self.sucess_upload_msg = "Successfully uploaded image"
        
    def test_landmarks_success(self):
        first_landmarks = [[301, 255], [218, 119]]
        self.payload['filedata'] = self.encoded_string_face
        response = self.client.post('/landmark_extraction', data=self.payload)
        result = response.json()
        self.assertIn('land_marks', result)
        self.assertIn('message', result)
        
        for row, l_coords in enumerate(first_landmarks): 
            self.assertEqual(
                int(result['land_marks'][0]['landmark_2d_106'][row][0]), 
                l_coords[0]
            )
            self.assertEqual(
                int(result['land_marks'][0]['landmark_2d_106'][row][1]), 
                l_coords[1]
            )
        self.assertEqual(result['message'], self.sucess_upload_msg)
    
    def test_landmarks_no_face(self):
        self.payload['filedata'] = self.encoded_string_no_face
        response = self.client.post('/landmark_extraction', data=self.payload)
        result = response.json()
        self.assertIn('land_marks', result)
        self.assertIn('message', result)
        self.assertEqual(result['land_marks'], [])
        self.assertEqual(result['message'], self.sucess_upload_msg)

    def test_landmarks_exception_no_bytes(self):
        self.payload['filedata'] = self.encoded_string_no_face
        response = self.client.post('/landmark_extraction', data="")
        result = response.json()
        self.assertNotIn('land_marks', result)
        self.assertNotIn('land_marks', result)

    def test_landmarks_exception_incorrect_bytes(self):
        self.payload['filedata'] = self.encoded_string_face[0:10]
        response = self.client.post('/landmark_extraction', data=self.payload)
        result = response.json()
        self.assertIn('land_marks', result)
        self.assertIn('message', result)
        self.assertEqual(result['land_marks'], [])
        self.assertEqual(result['message'], 'Exception raised Incorrect padding')

class TestEndpointsCropFace(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        
        path_to_img = "images_client/single_face.jpg"
        with open(path_to_img, "rb") as image_file:
            self.encoded_string_face = base64.b64encode(image_file.read())

        path_to_img = "images_client/no_face.jpg"
        with open(path_to_img, "rb") as image_file:
            self.encoded_string_no_face = base64.b64encode(image_file.read())

        self.payload = {"filedata": None}
        self.sucess_upload_msg = "Successfully uploaded image"
        
    def test_crop_success(self):
        self.payload['filedata'] = self.encoded_string_face
        response = self.client.post('/crop_face', data=self.payload)
        result = response.json()
        self.assertIn('cropped_image', result)
        self.assertIn('message', result)

        if len(result['cropped_image']) > 0:
            obj_reconstituted = pickle.loads(codecs.decode(result['cropped_image'][0].encode('latin1'), "base64"))
            crop = obj_reconstituted
        self.assertEqual(crop.shape, (208, 163, 3))

    def test_crop_no_face(self):
        self.payload['filedata'] = self.encoded_string_no_face
        response = self.client.post('/crop_face', data=self.payload)
        result = response.json()
        self.assertIn('cropped_image', result)
        self.assertIn('message', result)
        self.assertEqual(result['cropped_image'], [])

if __name__ == '__main__':
    unittest.main()