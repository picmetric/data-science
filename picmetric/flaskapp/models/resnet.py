#!/usr/bin/env python

import numpy

from tensorflow.keras.preprocessing import image
from tensorflow.python.keras.backend import set_session
# from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
# from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.applications.resnet_v2 import ResNet152V2


def instantiate_model():
	return (ResNet152V2(weights='imagenet'))


def load(img_path):
	return (image.load_img(img_path, target_size=(224, 224)))


def preprocess(img):
	arr = image.img_to_array(img)
	expanded = numpy.expand_dims(arr, axis=0)
	preprocessed = preprocess_input(expanded)
	return (preprocessed)


def predict(img_path: str, persistent: 'Persistent', classification_threshold: float = 0.3) -> dict:
	x = preprocess(load(img_path))
	feats = persistent.predict_model('resnet', x)
	results = decode_predictions(feats)[0]
	output = [
		{
			'object': str(pred[1]),
			'confidence': str(pred[2]),
		} for pred in results if pred[2] >= classification_threshold
	]

	return (output)



