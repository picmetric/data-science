from flask import Blueprint, jsonify, request, render_template
from flask import current_app as app

from flaskapp.models.persist import Persistent, download
from flaskapp.models import resnet, yolo

api = Blueprint('api', __name__)

@api.route("/api", methods=['GET', 'POST'])
def run_models():
	vals = request.get_json()
	url = vals.get('url', None)
	threshold = float(vals.get('threshold', 0.2))

	try:
		img_path = download(url)
	except Exception as e:
		return jsonify({
			'success': 'false',
			'errortype': 'InvalidURL',
			'parameters': {
				'url': url,
			},
			'message': f'Unable to retrieve url: {url}',
		})

	resnet_results = resnet.predict(img_path, app.config['persistent'], classification_threshold=threshold)
	yolo_results = yolo.predict(img_path, app.config['persistent'], classification_threshold=threshold)

	results = {
		'success': 'true',
		'url': str(url),
		'resnet50_objects': resnet_results,
		'yolo_objects': yolo_results,
	}

	return(jsonify(results))