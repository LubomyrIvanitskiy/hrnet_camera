from PIL import Image
from pose_estimator import predict_image_points
import numpy


class ImageProcessor(object):
    def __init__(self):
        pass

    def process(self, img):
        open_cv_image = numpy.array(img)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        predicted = predict_image_points(open_cv_image)
        im_pil = Image.fromarray(predicted)
        return im_pil
