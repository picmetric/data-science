#!/usr/bin/env python

from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from decouple import config

models = {}
lock = Lock()

def exists(model_name):
	with lock:
		return model_name in models

def get_model(model_name: str):
	with lock:
		return models.get(model_name, None)

def set_model(model_name: str, model):
	with lock:
		models[model_name] = model


manager = BaseManager(('', config('MANAGER_PORT', cast=int)), bytes(config('MANAGER_AUTHKEY'), encoding='utf8'))
manager.register('get_model', get_model)
manager.register('set_model', set_model)
manager.register('exists', exists)
server = manager.get_server()
server.serve_forever()
