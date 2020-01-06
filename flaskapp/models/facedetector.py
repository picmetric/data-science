"""Function to detect faces in an image"""

# import necessary libraries
from matplotlib import pyplot
from PIL import Image
from numpy import asarray
from mtcnn.mtcnn import MTCNN
import os
import shutil


# instantiate detector class. default weights
detector = MTCNN()

def count_faces(filename_or_url, user_id, image_id):
    """Count individual faces in an image"""
    pixels = pyplot.imread(filename_or_url)
    # detect faces in the image
    results = detector.detect_faces(pixels)
    count = str(len(results))
