from poremetrics import largest_region
from . import shapes
import numpy as np
import matplotlib.pyplot as plt
import cv2

def test_remove_small_from_medium():
    original_rectangle = shapes.make_rectangle()
    rectangle_with_small_feature = original_rectangle.copy()
    rectangle_with_small_feature[0:50,0:50]=255
    recreated_rectangle = largest_region(rectangle_with_small_feature)
    np.testing.assert_array_equal(recreated_rectangle,original_rectangle)
def test_remove_small_from_large():
    original_rectangle = shapes.make_rectangle(array_size=1024,x_length=900,y_length=900)
    rectangle_with_small_feature = original_rectangle.copy()
    rectangle_with_small_feature[0:20,0:20]=255
    recreated_rectangle = largest_region(rectangle_with_small_feature)
    np.testing.assert_array_equal(recreated_rectangle, original_rectangle)
