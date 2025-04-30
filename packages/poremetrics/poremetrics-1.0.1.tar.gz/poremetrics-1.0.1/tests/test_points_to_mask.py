from poremetrics import points_to_mask
import numpy as np
import pytest
from . import shapes
from . import parameters

s = 100
x=300
l = 1024
expected = np.zeros((l,l),dtype=np.uint8)
expected[s:x,s:x]=255

def test_array():
    points = np.array([[s, s], [s, x], [x, x], [x, s]], dtype=np.int32)  # Fixed point order
    output = points_to_mask(points, expected.shape)
    
    # Small percentage of pixels can be different
    difference = np.count_nonzero(output != expected)
    fraction_different = difference / expected.size
    assert fraction_different < parameters.BOUND_SCALE
    
    # Recreation is above a certain threshold
    output_binary = output > 0
    expected_binary = expected > 0
    intersection = np.logical_and(output_binary, expected_binary)
    union = np.logical_or(output_binary, expected_binary)
    iou = np.sum(intersection) / np.sum(union)
    assert iou > parameters.LOWER_BOUND_SCALE
    
def test_shape():
    points = np.array([[s,s],[s,x],[x,x],[x,s]],dtype=np.int32)
    output = points_to_mask(points, shape=(l, l))
    difference = np.count_nonzero(output!=expected)
    fraction_different = difference/expected.size
    assert fraction_different < parameters.BOUND_SCALE

    output_binary = output > 0
    expected_binary = expected >0
    intersection = np.logical_and(output_binary, expected_binary)
    union = np.logical_or(output_binary, expected_binary)
    iou = np.sum(intersection)/np.sum(union) 
    assert iou > parameters.LOWER_BOUND_SCALE

def test_neg_points():
    points = np.array([[-1, 2], [3, 4]],dtype=np.int32)
    with pytest.raises(ValueError):
        points_to_mask(points,shape=(10,10)) 
