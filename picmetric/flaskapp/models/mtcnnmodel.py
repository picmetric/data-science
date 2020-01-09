#!/usr/bin/env python

import numpy
import cv2

# Note that this lets us pass in the correct image data type
# It is functionally identical to tensorflow_core.keras.preprocessing.image.load_img
from flaskapp.models.utils.image import load_img_from_bytes
from flaskapp.models.mtcnn.mtcnn import MTCNN
from decouple import config


def instantiate_model():
	return (MTCNN(min_face_size=10, steps_threshold=[.3, .4, .4]))


def predict(img_bytes, persistent: 'Persistent', classification_threshold: float = 0.3) -> dict:
	x = cv2.imdecode(numpy.fromstring(img_bytes.getvalue(), numpy.uint8), 1)
	feats = persistent.predict_model('mtcnn', x)

	output = []

	for face in feats:
		if face['confidence'] < classification_threshold:
			continue

		outface = {
			'confidence': face['confidence'],
			'bounding_box': {
				'x_min': face['box'][0],
				'x_max': face['box'][0] + face['box'][2],
				'y_min': face['box'][1],
				'y_max': face['box'][1] + face['box'][3],
			},
			'keypoints': face['keypoints'],
		}
		output.append(outface)

	return (output)



