import cv2

def get_face(image):
    """Extracts face region from image using Haar Cascade."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        raise IndexError("No face detected")

    # Take first face
    (x, y, w, h) = faces[0]
    return image[y:y+h, x:x+w]
