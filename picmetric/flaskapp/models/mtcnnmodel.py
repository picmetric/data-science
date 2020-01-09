#!/usr/bin/env python

import numpy
import cv2

# Note that this lets us pass in the correct image data type
# It is functionally identical to tensorflow_core.keras.preprocessing.image.load_img
from flaskapp.models.utils.image import load_img_from_bytes
from flaskapp.models.mtcnn.mtcnn import MTCNN


def instantiate_model():
	# TODO: Return mtcnn model with standard model.predict(X) function
	return (MTCNN())


def predict(img_bytes, persistent: 'Persistent', classification_threshold: float = 0.3) -> dict:
	x = cv2.imdecode(np.fromstring(img_bytes.read(), numpy.uint8), 1)
	feats = persistent.predict_model('mtcnn', x)

	output = {feats}

	return (output)



