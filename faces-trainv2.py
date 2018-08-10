import os
import numpy as np
import cv2
import argparse
from PIL import Image
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb

import pickle
import imutils
import dlib


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required = True, help ="path to facial landmark")
args = vars(ap.parse_args())

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])
fa = FaceAligner(predictor, desiredFaceWidth=256)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "images")

face_cascade = cv2.CascadeClassifier('/home/odroid/opencv-3.4.0/data/haarcascades/haarcascade_frontalface_alt2.xml')
#recognizer = cv2.LBPHFaceRecognizer()
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(image_dir):
	for file in files:
		if file.endswith("png") or file.endswith("jpg"):
			path = os.path.join(root, file)
			label = os.path.basename(root).replace(" ", "-").lower()
			print(label, path)

			if not label in label_ids:
				label_ids[label] = current_id
				current_id+=1
			id_ = label_ids[label]
			print(label_ids)


			#x_train.append(path)
			#y_labels.append(label)

			pil_images = Image.open(path)
			gr = pil_images.convert("L")
			size = (300,300)
			final_image = gr.resize(size, Image.ANTIALIAS)
			#img_align = fa.align(final_image, gr)
			image_array = np.array(final_image, "uint8")
			#print(image_array)
			
			faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)
			rects = detector(gr, 2)
			#for(x,y,w,h) in faces:
				#roi = image_array[y:y+h, x:x+w]
				#x_train.append(roi)
				#y_labels.append(id_)
				
			for rect in rects:
				(x,y,w,h) = rect_to_bb(rect)
				roi = image_array[y:y+h, x:x+w]
				x_train.append(roi)
				y_labels.append(id_)
				img_align = fa.align(roi, rect)

#print(x_train)
#print(y_labels)

with open("labels.pickle", "wb") as f:
	pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainerv2.yml")



