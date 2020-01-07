from flask import Blueprint, jsonify, request, render_template

api = Blueprint('api', __name__)

@api.route("/api", methods=['GET', 'POST'])
def run_models():
    APP_LOG.info(f'''/api called, request values: {request.values}''')
    url = request.values.get('url', None)
    threshold = float(request.values.get('threshold', 0.2))

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

    APP_LOG.info('Image retrieved.')
    APP_LOG.info('Running resnet50...')
    resnet_results = resnet.predict(img_path, persistent, classification_threshold=threshold)
    APP_LOG.info('Done resnet50.')
    APP_LOG.info('Running YOLOv3...')
    yolo_results = yolo.predict(img_path, persistent, classification_threshold=threshold)
    APP_LOG.info('Done YOLOv3.')

    results = {
        'success': 'true',
        'url': str(url),
        'resnet50_objects': resnet_results,
        'yolo_objects': yolo_results,
    }
    APP_LOG.info(f'Done predicting for image at url: {url}')

    return(jsonify(results))