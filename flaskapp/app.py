#!/usr/bin/env python

import logging

from flask import Flask, jsonify, request
from log import startLog, LOGFILE
from models.persist import Persistent, download
from models import resnet


startLog(LOGFILE)
APP_LOG = logging.getLogger('root')

APP_LOG.info('Creating app...')
app = Flask(__name__)
APP_LOG.info('Creating persistent object...')
persistent = Persistent()
APP_LOG.info('Flask instantiation complete.')


@app.route("/api", methods=['GET', 'POST'])
def api():
	APP_LOG.info(f'''/api called, request values:
{request.values}''')
	url = request.values.get('url', None)

	try:
		img_path = download(url)
	except Exception as e:
		APP_LOG.warning(f'Failed to retrieve image at url: {url}')
		APP_LOG.warning(e)
		return jsonify({
			'success': 'false',
			'errortype': 'InvalidURL',
			'parameters': {
				'url': url,
			},
			'message': f'Unable to retrieve url: {url}',
		})

	APP_LOG.info('Image retrieved, loading predictions...')
	resnet_results = resnet.predict(img_path, persistent)

	results = {
		'success': 'true',
		'url': str(url),
		'resnet50_objects': resnet_results,
	}
	APP_LOG.info(f'Done predicting for image at url: {url}')

	return(jsonify(results))


# Debug purposes only
if __name__ == '__main__':
	app.run()
