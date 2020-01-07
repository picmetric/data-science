#!/usr/bin/env python

import logging

from flask import Flask, jsonify, request, render_template, redirect

from flaskapp.models.persist import Persistent
from flaskapp.routes.api import api
from flaskapp.extensions import debug_toolbar

def create_app(settings_override=None):
	app = Flask(__name__, instance_relative_config=True)

	app.config.from_object('config.settings')
	app.config['persistent'] = Persistent()
	app.register_blueprint(api)
	extensions(app)

	@app.route('/')
	def index():
		return render_template('base.html')

	@app.route('/apitest')
	def apitest():
		return redirect('/static/apitest.html')

	return app

def extensions(app):
    debug_toolbar.init_app(app)

    return None