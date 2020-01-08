#!/usr/bin/env python

import logging
import requests
import io

from urllib.request import urlretrieve
from . import resnet, yolo
from decouple import config
from multiprocessing.managers import BaseManager


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
		self.modelmanager = BaseManager(('', config('MANAGER_PORT', cast=int)), bytes(config('MANAGER_AUTHKEY'), encoding='utf8'))
		self.modelmanager.register('get_model')
		self.modelmanager.register('set_model')
		self.modelmanager.register('exists')
		self.modelmanager.connect()
		self.instantiate_models(self.modelmanager)
		# PERSIST_LOG.info(
		print('Done loading models.')

	def instantiate_models(self, modelmanager):
		# PERSIST_LOG.info(
		print('Checking for resnet...')
		# self.models['resnet']
		if modelmanager.exists('resnet'):
			print('Resnet not found, instantiating...')
			modelmanager.set_model('resnet', resnet.instantiate_model())
		# resnet = modelmanager.get_model('resnet')
		# PERSIST_LOG.info(
		print('Done loading resnet.')

		# PERSIST_LOG.info(
		print('Checking for YOLOv3...')
		if modelmanager.exists('yolo'):
			print('yolo not found, instantiating...')
			modelmanager.set_model('yolo', yolo.instantiate_model(yolo.YOLO_WEIGHTS_PATH))
		# self.models['yolo'] = modelmanager.get_model('resnet', resnet.instantiate_model, yolo.YOLO_WEIGHTS_PATH)
		# PERSIST_LOG.info(
		print('Done loading YOLOv3.')

	def predict_model(self, model, x):
		if isinstance(model, str):
			model = self.modelmanager.get_model(model)

		predictions = model.predict(x)

		return (predictions)

