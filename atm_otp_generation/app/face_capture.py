import cv2
import os
import logging as log
import random
import string
import datetime as dt
from time import sleep
from django.conf import settings

cascPath = os.path.join(settings.BASE_DIR, "haarcascade_frontalface_default.xml")
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log', level=log.INFO)
image_dir = os.path.join(settings.BASE_DIR, "media")

def main():
    file_name = ''.join(random.choices(string.ascii_uppercase, k=3))
    img_file_name = f"{file_name}.jpg"
    video_capture = cv2.VideoCapture(0)
    anterior = 0
    try:
        while True:
            if not video_capture.isOpened():
                print('Unable to load camera.')
                sleep(5)
                continue
            ret, frame = video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

            if anterior != len(faces):
                anterior = len(faces)
                log.info("faces: " + str(len(faces)) + " at " + str(dt.datetime.now()))

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite(os.path.join(image_dir, img_file_name), frame)
                break
    except Exception as e:
        print(e)
    finally:
        video_capture.release()
        cv2.destroyAllWindows()
    return img_file_name
