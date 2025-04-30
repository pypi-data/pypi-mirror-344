import cv2
import numpy as np
from .find_area import find_area

def extract_largest_object(img: np.array,save_label=None):
    _, label = cv2.connectedComponents(img)
    values, counts = np.unique(label, return_counts=True)
    # Can print the label if that's more desirable. This is mostly for debugging
    if save_label!=None:
        cv2.imwrite(save_label,label*float(255/label.max()))

    # Need to remove the blank values from the unique values
    null_position = np.where(values==0)
    counts_clean = np.delete(counts, null_position)
    values_clean = np.delete(values, null_position)
    # Removed values
    if len(values) > 1:
        # Find the object with the most pixels
        max_position = np.argmax(counts_clean)
        max_val = values_clean[max_position]
        filter_values = np.where(label==max_val,255,0).astype(dtype=np.uint8)
        return filter_values
    else:
        return label.astype(dtype=np.uint8)*255
