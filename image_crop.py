import cv2
import numpy as np


class Scanner(object):
    def __init__(self):
        image, dst = self.detect_edge()

    def detect_edge(self):
        dst = None
        print('reading')
        image = cv2.imread("sample.jpg")
        orig = image.copy()
        cv2.imshow("Title", image)
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print('grayed')
        cv2.imshow("Title", gray)
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            x = x - 25  # Padding trick to take the whole face not just Haarcascades points
            y = y - 40  # Same here...
            cv2.rectangle(image, (x, y), (x + w + 50, y + h + 70), (27, 200, 10), 2)
            cv2.imshow('Face Detection', image)
            while True:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        for (x, y, width, height) in faces:
            roi = image[y:y + height, x:x + width]
            cv2.imwrite("face.png", roi)

        return image, dst

if __name__ == '__main__':
    scan = Scanner()