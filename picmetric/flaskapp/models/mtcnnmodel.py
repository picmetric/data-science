#!/usr/bin/env python

import numpy

# Note that this lets us pass in the correct image data type
# It is functionally identical to tensorflow_core.keras.preprocessing.image.load_img
from flaskapp.models.utils.image import load_img_from_bytes


def instantiate_model():
	# TODO: Return mtcnn model with standard model.predict(X) function
	return ()


def predict(img_bytes, persistent: 'Persistent', classification_threshold: float = 0.3) -> dict:
	x = None # TODO: Convert img_bytes to proper x input data, as an array
	feats = persistent.predict_model('resnet', x) # This just calls model.predict(x)

	output = {} # TODO: Populate this dict with our results

	return (output)



