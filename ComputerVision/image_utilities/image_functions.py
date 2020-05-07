import cv2

def load_image(filename, flags=None):
    return cv2.imread(filename, flags)

def get_image_dimensions(image):
    return image.shape