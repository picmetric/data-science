# Modified code from https://github.com/keras-team/keras-preprocessing

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io
import os
import warnings

import numpy as np

try:
	from PIL import ImageEnhance
	from PIL import Image as pil_image
except ImportError:
	pil_image = None
	ImageEnhance = None


if pil_image is not None:
	_PIL_INTERPOLATION_METHODS = {
		'nearest': pil_image.NEAREST,
		'bilinear': pil_image.BILINEAR,
		'bicubic': pil_image.BICUBIC,
	}
	# These methods were only introduced in version 3.4.0 (2016).
	if hasattr(pil_image, 'HAMMING'):
		_PIL_INTERPOLATION_METHODS['hamming'] = pil_image.HAMMING
	if hasattr(pil_image, 'BOX'):
		_PIL_INTERPOLATION_METHODS['box'] = pil_image.BOX
	# This method is new in version 1.1.3 (2013).
	if hasattr(pil_image, 'LANCZOS'):
		_PIL_INTERPOLATION_METHODS['lanczos'] = pil_image.LANCZOS

def load_img_from_bytes(bytes_img, grayscale=False, color_mode='rgb', target_size=None,
			 interpolation='nearest'):
	"""Loads an image into PIL format.
	# Arguments
		path: Path to image file.
		grayscale: DEPRECATED use `color_mode="grayscale"`.
		color_mode: The desired image format. One of "grayscale", "rgb", "rgba".
			"grayscale" supports 8-bit images and 32-bit signed integer images.
			Default: "rgb".
		target_size: Either `None` (default to original size)
			or tuple of ints `(img_height, img_width)`.
		interpolation: Interpolation method used to resample the image if the
			target size is different from that of the loaded image.
			Supported methods are "nearest", "bilinear", and "bicubic".
			If PIL version 1.1.3 or newer is installed, "lanczos" is also
			supported. If PIL version 3.4.0 or newer is installed, "box" and
			"hamming" are also supported.
			Default: "nearest".
	# Returns
		A PIL Image instance.
	# Raises
		ImportError: if PIL is not available.
		ValueError: if interpolation method is not supported.
	"""
	if grayscale is True:
		warnings.warn('grayscale is deprecated. Please use '
						'color_mode = "grayscale"')
		color_mode = 'grayscale'
	if pil_image is None:
		raise ImportError('Could not import PIL.Image. '
							'The use of `load_img` requires PIL.')
	img = pil_image.open(bytes_img)
	if color_mode == 'grayscale':
		# if image is not already an 8-bit, 16-bit or 32-bit grayscale image
		# convert it to an 8-bit grayscale image.
		if img.mode not in ('L', 'I;16', 'I'):
			img = img.convert('L')
	elif color_mode == 'rgba':
		if img.mode != 'RGBA':
			img = img.convert('RGBA')
	elif color_mode == 'rgb':
		if img.mode != 'RGB':
			img = img.convert('RGB')
	else:
		raise ValueError('color_mode must be "grayscale", "rgb", or "rgba"')
	if target_size is not None:
		width_height_tuple = (target_size[1], target_size[0])
		if img.size != width_height_tuple:
			if interpolation not in _PIL_INTERPOLATION_METHODS:
				raise ValueError(
					'Invalid interpolation method {} specified. Supported '
					'methods are {}'.format(
						interpolation,
						", ".join(_PIL_INTERPOLATION_METHODS.keys())))
			resample = _PIL_INTERPOLATION_METHODS[interpolation]
			img = img.resize(width_height_tuple, resample)
	return img

