
import numpy as np
import cv2

def img_to_encoding(face_img, model=None):
    """
    Convert face image to an embedding (feature vector).
    For demo, flatten + normalize image.
    Replace with FaceNet/DeepFace model in production.
    """
    face_img = cv2.resize(face_img, (96, 96))  # standard size
    encoding = face_img.flatten() / 255.0
    return np.array(encoding)
