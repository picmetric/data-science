#!/usr/bin/env python

import numpy, os

from decouple import config
from tensorflow_core.keras.models import load_model
from tensorflow_core.keras.preprocessing import image
from flaskapp.models.utils.image import load_img_from_bytes


YOLO_WEIGHTS_URL = "https://pjreddie.com/media/files/yolov3.weights"
YOLO_WEIGHTS_PATH = "./flaskapp/models/weights/yolo.h5"
YOLO_CLASSES_PATH = "./flaskapp/models/weights/coco_classes.txt"
YOLO_ANCHORS = [
	[116, 90, 156, 198, 373, 326],
	[30, 61, 62, 45, 59, 119],
	[10, 13, 16, 30, 33, 23],
]
YOLO_SIZE = (416, 416)


def instantiate_model(model_path=None):
	if model_path is None:
		model_path = './flaskapp/models/weights/yolo.h5'
	# import os
	# print(os.getcwd())
	return (load_model(model_path))


def load_classes(classes_path):
	with open(classes_path, 'r') as f:
		classes = f.readlines()
	cleaned_classes = [s.rstrip('\n') for s in classes]
	return (cleaned_classes)


def load(img_bytes, target_size=YOLO_SIZE):
	img = load_img_from_bytes(img_bytes)
	original_size = img.size

	img = load_img_from_bytes(img_bytes, target_size=target_size)
	return (img, original_size)


def preprocess(img):
	arr = image.img_to_array(img)
	scaled = arr.astype('float32') / 255.
	expanded = numpy.expand_dims(scaled, axis=0)
	return (expanded)


def sigmoid(x):
	return 1. / (1. + numpy.exp(-x))


class BoundBox:
	def __init__(self, xmin, ymin, xmax, ymax, objness, classes):
		self.xmin = xmin
		self.ymin = ymin
		self.xmax = xmax
		self.ymax = ymax
		self.objness = objness
		self.classes = classes
		self.label = None
		self.score = None
		self.text_label = None
		self.get_score()

	def get_overlap(self, other):
		return (bbox_iou(self, other))

	def get_label(self):
		if self.label is None:
			self.label = numpy.argmax(self.classes)

		return self.label

	def get_score(self):
		if self.score is None:
			self.score = self.classes[self.get_label()]

		return self.score

	def get_text_label(self, text_labels):
		if self.text_label is None:
			self.text_label = text_labels[self.label]

		return self.text_label

	def to_dict(self, original_size, text_labels):
		d = {
			"object": self.get_text_label(text_labels),
			"confidence": str(self.get_score()),
			"bounding_box": {
				"x_min": str(self.xmin * original_size[0]),
				"x_max": str(self.xmax * original_size[0]),
				"y_min": str(self.ymin * original_size[1]),
				"y_max": str(self.ymax * original_size[1]),
			},
		}

		return (d)


def decode_output(prediction, anchors, obj_threshold=0.3, net_size=YOLO_SIZE):
	# Most of this code courtesy of https://github.com/experiencor/keras-yolo3/
	# TODO: Make this check for classification thresholds more efficiently
	net_w, net_h = net_size
	grid_h, grid_w = prediction.shape[:2]
	nb_box = 3
	prediction = prediction.reshape((grid_h, grid_w, nb_box, -1))
	nb_class = prediction.shape[-1] - 5

	boxes = []

	prediction[..., :2]  = sigmoid(prediction[..., :2])
	prediction[..., 4:]  = sigmoid(prediction[..., 4:])
	prediction[..., 5:]  = prediction[..., 4][..., numpy.newaxis] * prediction[..., 5:]
	prediction[..., 5:] *= prediction[..., 5:] > obj_threshold

	for i in range(grid_h * grid_w):
		row = i / grid_w
		col = i % grid_w

		for b in range(nb_box):
			# 4th element is objectness score
			objectness = prediction[int(row)][int(col)][b][4]
			# objectness = prediction[..., :4]

			if(objectness.all() <= obj_threshold):
				continue

			# first 4 elements are x, y, w, and h
			x, y, w, h = prediction[int(row)][int(col)][b][:4]

			x = (col + x) / grid_w  # center position, unit: image width
			y = (row + y) / grid_h  # center position, unit: image height
			w = anchors[2 * b + 0] * numpy.exp(w) / net_w  # unit: image width
			h = anchors[2 * b + 1] * numpy.exp(h) / net_h  # unit: image height

			# last elements are class probabilities
			classes = prediction[int(row)][col][b][5:]

			for c in classes:
				if c > obj_threshold:
					box = BoundBox(x-w/2, y-h/2, x+w/2, y+h/2, objectness, classes)
					# box = BoundBox(x-w/2, y-h/2, x+w/2, y+h/2, None, classes)

					boxes.append(box)

					break

	return boxes


def _interval_overlap(interval_a, interval_b):
	# This code courtesy of https://github.com/experiencor/keras-yolo3/
	x1, x2 = interval_a
	x3, x4 = interval_b
	if x3 < x1:
		if x4 < x1:
			return 0
		else:
			return min(x2, x4) - x1
	else:
		if x2 < x3:
			return 0
		else:
			return min(x2, x4) - x3


def bbox_iou(box1, box2):
	# This code courtesy of https://github.com/experiencor/keras-yolo3/
	intersect_w = _interval_overlap([box1.xmin, box1.xmax], [box2.xmin, box2.xmax])
	intersect_h = _interval_overlap([box1.ymin, box1.ymax], [box2.ymin, box2.ymax])
	intersect = intersect_w * intersect_h
	w1, h1 = box1.xmax - box1.xmin, box1.ymax - box1.ymin
	w2, h2 = box2.xmax - box2.xmin, box2.ymax - box2.ymin
	union = w1 * h1 + w2 * h2 - intersect
	return float(intersect) / union


def predict(
		img_bytes,
		persistent: 'Persistent',
		overlap_threshold: float = 0.5,
		classification_threshold: float = 0.3,
	) -> dict:

	img, original_size = load(img_bytes)
	x = preprocess(img)
	pred = persistent.predict_model('yolo', x)

	text_labels = load_classes(YOLO_CLASSES_PATH)

	# TODO: Make this work properly for boxes with multiple classifications above the threshold

	boxes = []
	for i in range(len(pred)):
		# decode the output of the network
		boxes += decode_output(pred[i][0], YOLO_ANCHORS[i], obj_threshold=classification_threshold)

	# Remove duplicate boxen
	cleaned_boxes = []
	for box in sorted(boxes, key=lambda x: x.get_score(), reverse=True):
		for cleaned_box in cleaned_boxes:
			if (box.get_label() == cleaned_box.get_label() and
					box.get_overlap(cleaned_box) > overlap_threshold):
				break
		else:
			cleaned_boxes.append(box)

	output = [
		box.to_dict(original_size, text_labels) for box in cleaned_boxes
	]

	return (output)

