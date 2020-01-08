#!/usr/bin/env python

import logging
import requests
import io
import numpy

from urllib.request import urlretrieve
from . import resnet, yolo
from decouple import config
from multiprocessing.managers import BaseManager


class Non200ResponseError(Exception): pass
# PERSIST_LOG = logging.getLogger('root')


def retrieve_as_bytes(img_url):
	print(f'Retrieving image at url: {img_url} ...')
	with requests.get(img_url) as response:
		if response.status_code != 200:
			raise Non200ResponseError(
				f'Received response with status code {response.status_code} while fetching url: {img_url}'
			)
		bytes_content = io.BytesIO(response.content)
	# PERSIST_LOG.info(
	print(f'''Downloaded image at url: {img_url}''')
	return (bytes_content)

class Persistent:
	def __init__(self):
		self.models = {}
		self.modelmanager = BaseManager(('localhost', config('MANAGER_PORT', cast=int)), bytes(config('MANAGER_AUTHKEY'), encoding='utf8'))
		self.modelmanager.register('predict')
		self.modelmanager.register('instantiate')
		self.modelmanager.register('exists')
		self.modelmanager.connect()
		self.instantiate_models(self.modelmanager)
		# PERSIST_LOG.info(
		print('Done loading models.')

	def instantiate_models(self, modelmanager):
		# PERSIST_LOG.info(
		print('Checking for resnet...')
		# self.models['resnet']
		if modelmanager.exists('resnet')._getvalue() is False:
			print('Resnet not found, instantiating...')
			modelmanager.instantiate('resnet')
			print('Done loading resnet.')
		else:
			print('resnet already loaded.')
		# resnet = modelmanager.get_model('resnet')
		# PERSIST_LOG.info(

		# PERSIST_LOG.info(
		print('Checking for YOLOv3...')
		if modelmanager.exists('yolo')._getvalue() is False:
			print('yolo not found, instantiating...')
			modelmanager.instantiate('yolo')
			print('Done loading YOLOv3.')
		else:
			print('yolo already loaded.')
		# self.models['yolo'] = modelmanager.get_model('resnet', resnet.instantiate_model, yolo.YOLO_WEIGHTS_PATH)
		# PERSIST_LOG.info(

	def predict_model(self, model, x):
		predictions = self.modelmanager.predict(model, x)._getvalue()

		return predictions

