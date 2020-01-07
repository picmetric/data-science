#!/usr/bin/env python

import logging

from flask import Flask, jsonify, request
from log import startLog, LOGFILE

from .models.persist import Persistent, download
from .models import resnet, yolo
from .routes.api import api

def create_app(settings_override=None):
	startLog(LOGFILE)
	APP_LOG = logging.getLogger('root')

	APP_LOG.info('Creating app...')
	app = Flask(__name__, instance_relative_config=True)

	app.config.from_object('config.settings')

	APP_LOG.info('Creating persistent object...')
	persistent = Persistent()
	APP_LOG.info('Flask instantiation complete.')

	app.register_blueprint(api)

    @app.route('/')
    def redir():
        return render_template('base.html')

	return app
