#!/usr/bin/env python

from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from decouple import config
from flaskapp.models import yolo, resnet

model_modules = {
	'yolo': yolo,
	'resnet': resnet,
}
models = {}
lock = Lock()


def predict(model_name, x):
	with lock:
		result = models[model_name].predict(x)
		return result


def exists(model_name):
	with lock:
		return model_name in models


def instantiate(model_name):
	with lock:
		model_module = model_modules[model_name]
		model = model_module.instantiate_model()
		models[model_name] = model


def main():
	for model_name, model_module in model_modules.items():
		print(f'Instantiating {model_name}...')
		models[model_name] = model_module.instantiate_model()
	print('Done initial model instantiation.')
	manager = BaseManager(('localhost', config('MANAGER_PORT', cast=int)), bytes(config('MANAGER_AUTHKEY'), encoding='utf8'))
	manager.register('instantiate', instantiate)
	manager.register('predict', predict)
	manager.register('exists', exists)
	server = manager.get_server()
	server.serve_forever()


if __name__ == '__main__':
	main()
