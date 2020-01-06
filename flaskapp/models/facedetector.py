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

# extract a single face from a given photograph
def extract_faces(filename_or_orl):
    # load image from file

    # Actual code
    pixels = pyplot.imread(filename_or_orl)

    # detect faces in the image
    results = detector.detect_faces(pixels)
    i = 0
    for result in results:
        # insert face only if confidence is greater than 99%
        if(result['confidence'] > 0.99):
            face_x, face_y, width, height = result['box']
            # check for negative index
            if((face_x > 0) & (face_y > 0)):
                face = pixels[face_y:face_y + height, face_x:face_x + width]
                face_image = Image.fromarray(face)
                face_image.save(f'{i}.jpg')

    return f'{i} faces have been detected in the given image'

# # load the photo and extract the face
# extract_faces('people.jpg')
