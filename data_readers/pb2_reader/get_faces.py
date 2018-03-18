import cv2
from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='return positions and sizes of faces')
parser.add_argument('path', metavar='image_path', type=str, help='path to procesiing image')
args = parser.parse_args()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
img = cv2.imread(args.path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
print(faces)