from flask import Blueprint, jsonify, request, render_template
from flask import current_app as app

from flaskapp.models.persist import Persistent, download
from flaskapp.models import resnet, yolo

api = Blueprint('api', __name__)

@api.route("/api", methods=['GET', 'POST'])
def run_models():
	p = Persistent()
	vals = None
	try:
		vals = request.get_json()
		url = vals.get('url', None)
		threshold = max([float(vals.get('threshold', 0.2)), 0.01])
		# url = request.form.get('url')

		# url = request.json["url"]
		# threshold = .2
		
	except Exception as e:
		return jsonify({
			'success': 'false',
			'errortype': 'InvalidParameters',
			'parameters': vals,
			'message': f'Invalid or malformed parameters: {str(e)}',
		})

	try:
		img_path = download(url)
	except Exception as e:
		return jsonify({
			'success': 'false',
			'errortype': 'InvalidURL',
			'parameters': vals,
			'message': f'Unable to retrieve url: {url}',
		})

	resnet_results = resnet.predict(img_path, p, classification_threshold=threshold)
	yolo_results = yolo.predict(img_path, p, classification_threshold=threshold)

	results = {
		'success': 'true',
		'url': str(url),
		'resnet50_objects': resnet_results,
		'yolo_objects': yolo_results,
	}

	return(jsonify(results))