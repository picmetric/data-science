#!/usr/bin/env python

import logging

from urllib.request import urlretrieve
from tensorflow.keras.applications.resnet50 import ResNet50


PERSIST_LOG = logging.getLogger('root')


def download(img_url):
	local_filename, headers = urlretrieve(img_url)
	PERSIST_LOG.info(f'''Downloaded image at url: {img_url}
		Local filename: {local_filename}
		Headers:
{headers}''')
	return (local_filename)


class Persistent:
	def __init__(self):
		self.models = {}
		self.instantiate_models()
		PERSIST_LOG.info('Done loading models.')

	def instantiate_models(self):
		PERSIST_LOG.info('Loading resnet50...')
		self.models['resnet'] = ResNet50(weights='imagenet')
