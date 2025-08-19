import cv2
from deepface import DeepFace

def run(image_one, image_two, save_dest=None):
    """
    Compare two face images and return True if they belong to the same person.
    """
    print(f"{image_one=} {image_two=}")
    
    try:
        result = DeepFace.verify(img1_path=str(image_one), img2_path=str(image_two), enforce_detection=True)
        print(result)
        return result["verified"]   # True if same person
    except Exception as e:
        print(f"Error during face comparison: {e}")
        return False
