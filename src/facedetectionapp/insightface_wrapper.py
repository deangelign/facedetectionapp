from typing import Dict, List, Tuple

from insightface.app import FaceAnalysis
from numpy import ndarray


class FaceAnalyzer:
    def __init__(self):
        """
        Initializes the FaceDetector with the InsightFace model.
        """
        self.faceAnalyzer = FaceAnalysis(
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
        )
        self.faceAnalyzer.prepare(ctx_id=0, det_size=(640, 640))
        self.count = None

    def detect_face(self, image: ndarray) -> bool:
        """
        Detects if a face is present in the given image.

        Args:
            image (ndarray): Opencv RGB image.

        Returns:
            bool: True if a face is detected, False otherwise.
        """
        self.count = len(self.faceAnalyzer.get(image))
        return self.count > 0

    def extract_landmarks(self, image: ndarray) -> List[Dict[str, List[Tuple[float, float]]]]:
        """
        Extracts facial landmarks from the given image.

        Each element in the returned list contains a dictionary that store the landmarks, for
        a single face, over the key 'landmark_2d_106'. The landmarks are stored in 2D matrix
        format. These matrix always have 106 rows and 2 columns. Each row represents the 2D
        coordinates (x, y) for a landmark.

        Args:
            image (ndarray): Opencv RGB image.

        Returns:
            List[Dict[str, Tuple[float, float]]]: List of facial landmarks as pairs
            of (x, y) coordinates.
        """
        faces_info = self.faceAnalyzer.get(image)
        landmarks = [{"landmark_2d_106": face["landmark_2d_106"].tolist()} for face in faces_info]
        return landmarks

    def crop_face(self, image: ndarray) -> ndarray:
        """
        Crops the face from the given image.

        Args:
            image (bytes): Opencv RGB image.

        Returns:
            ndarray: Opencv RGB image.
        """
        faces_info = self.faceAnalyzer.get(image)
        if len(faces_info) == 0:
            return None
        x1, y1, x2, y2 = faces_info[0]["bbox"]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cropped_face = image[y1:y2, x1:x2].copy()
        return cropped_face
