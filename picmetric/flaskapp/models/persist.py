#!/usr/bin/env python

import logging
import requests
import io

from urllib.request import urlretrieve
from . import resnet, yolo


# PERSIST_LOG = logging.getLogger('root')


def download(img_url):
	print(f'Retrieving image at url: {img_url} ...')
	local_filename, headers = urlretrieve(img_url)
	# PERSIST_LOG.info(
	print(f'''Downloaded image at url: {img_url}
		Local filename: {local_filename}
		Headers:
{headers}''')
	return (local_filename)

def retrieve_as_bytes(img_url):
	print(f'Retrieving image at url: {img_url} ...')
	with requests.get(img_url) as response:
		bytes_content = io.BytesIO(response.content)
	# PERSIST_LOG.info(
	print(f'''Downloaded image at url: {img_url}''')
	return (bytes_content)

class Persistent:
	def __init__(self):
		self.models = {}
		self.instantiate_models()
		# PERSIST_LOG.info(
		print('Done loading models.')

	def instantiate_models(self):
		# PERSIST_LOG.info(
		print('Loading resnet50...')
		self.models['resnet'] = resnet.instantiate_model()
		# PERSIST_LOG.info(
		print('Done loading resnet50.')

		# PERSIST_LOG.info(
		print('Loading YOLOv3...')
		self.models['yolo'] = yolo.instantiate_model(yolo.YOLO_WEIGHTS_PATH)
		# PERSIST_LOG.info(
		print('Done loading YOLOv3.')

	def predict_model(self, model, x):
		if isinstance(model, str):
			model = self.models[model]

		predictions = model.predict(x)

		return (predictions)

