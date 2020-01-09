#!/usr/bin/env python

import logging, requests, io, time, os, numpy, sys, subprocess

from urllib.request import urlretrieve
from . import resnet, yolo
from decouple import config
from multiprocessing.managers import BaseManager


class Non200ResponseError(Exception): pass
class NoModelManagerError(Exception): pass
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
	def __init__(self, max_tries=5):
		self.models = {}
		self.modelmanager = self.connect_or_start_manager(max_tries=max_tries)
		self.instantiate_models(self.modelmanager)
		# PERSIST_LOG.info(

	def connect_or_start_manager(self, max_tries=5):
		for attempt in range(1, max_tries + 1):
			print(f'Connecting to modelmanager [try {attempt} of {max_tries}]...')
			try:
				manager = BaseManager(('localhost', config('MANAGER_PORT', cast=int)), bytes(config('MANAGER_AUTHKEY'), encoding='utf8'))
				manager.register('predict')
				manager.register('instantiate')
				manager.register('exists')
				manager.connect()
				print('Successfully connected to modelmanager.')
				return manager
			except ConnectionRefusedError as e:
				print(f'Failed to connect to modelmanager: {str(e)}')
				self.start_manager()
		raise NoModelManagerError(f'Unable to connect to modelmanager after {max_tries} tries.')

	def start_manager(self):
		print('Starting modelmanager...')
		# os.system('pipenv run python modelmanager.py > /dev/null 2>&1 < /dev/null & disown')
		with open(os.devnull, 'r+b', 0) as DEVNULL:
			subprocess.Popen(['nohup', sys.executable, 'modelmanager.py'],
				stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, close_fds=True, preexec_fn=os.setpgrp)
		print(f'modelmanager start command executed, sleeping 3 seconds...')
		time.sleep(3)
		print(f'Done sleeping.')

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
		print('Checking for yolo...')
		if modelmanager.exists('yolo')._getvalue() is False:
			print('yolo not found, instantiating...')
			print('working dir')
			print(os.path.isfile('./flaskapp/models/weights/yolo.h5'))
			print(os.path.isfile(config('YOLO_WEIGHTS_PATH')))
			modelmanager.instantiate('yolo')
			print('Done loading yolo.')
		else:
			print('yolo already loaded.')
		# self.models['yolo'] = modelmanager.get_model('resnet', resnet.instantiate_model, yolo.YOLO_WEIGHTS_PATH)
		# PERSIST_LOG.info(

	def predict_model(self, model, x):
		print(f'Predicting on model {model}...')
		predictions = self.modelmanager.predict(model, x)._getvalue()
		print(f'Done predicting on model {model}.')

		return predictions

