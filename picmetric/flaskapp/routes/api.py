from flask import Blueprint, jsonify, request, render_template
from flask import current_app as app

from flaskapp.models.persist import Persistent, retrieve_as_bytes
from flaskapp.models import resnet, yolo, mtcnnmodel

api = Blueprint('api', __name__)

@api.route("/api", methods=['GET', 'POST'])
def run_models():
	p = Persistent()
	vals = None
	try:
		vals = request.get_json()
		url = vals.get('url', None)
		threshold = max([float(vals.get('threshold', 0.2)), 0.01])
	except Exception as e:
		print(str(e.__traceback__))
		print(e)
		return jsonify({
			'success': 'false',
			'errortype': 'InvalidParameters',
			'parameters': vals,
			'message': f'Invalid or malformed parameters: {vals}',
			'exception': str(e),
		})

	try:
		img_bytes = retrieve_as_bytes(url)
	except Exception as e:
		print(str(e.__traceback__))
		print(e)
		return jsonify({
			'success': 'false',
			'errortype': 'InvalidURL',
			'parameters': vals,
			'message': f'Unable to retrieve url: {url}',
			'exception': str(e),
		})

	try:
		resnet_results = resnet.predict(img_bytes, p, classification_threshold=threshold)
		yolo_results = yolo.predict(img_bytes, p, classification_threshold=threshold)
		mtcnn_results = mtcnnmodel.predict(img_bytes, p, classification_threshold=threshold)
	except Exception as e:
		print(str(e.__traceback__))
		print(e)
		return jsonify({
			'success': 'false',
			'errortype': 'FailedPrediction',
			'parameters': vals,
			'message': f'Exception while retrieving predictions.',
			'exception': str(e),
		})

	results = {
		'success': 'true',
		'url': str(url),
		'resnet_objects': resnet_results,
		'yolo_objects': yolo_results,
		'mtcnn_faces': mtcnn_results,
	}

	return(jsonify(results))