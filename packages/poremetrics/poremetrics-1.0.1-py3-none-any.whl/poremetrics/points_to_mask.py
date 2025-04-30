import numpy as np
import cv2

def points_to_mask(points, shape):
    error_codes =False
    """
    Create a binary image (uint8) from a list of (x,y) coordinates.
    
    Parameters:
    -----------
    points : list or numpy.ndarray
        List of (x,y) coordinates or numpy array of shape (n,2)
    shape : tuple, optional
        Shape of the output image as (height, width)
    error_codes : bool, optional
        Whether to return human-readable error codes instead of raising exceptions.
        
    Returns:
    --------
    numpy.ndarray or tuple
        If successful, returns a uint8 numpy array with 1s at the specified points.
        If error_codes is True and an error occurs, returns a tuple (None, error_message).
        
    Error Codes:
    -----------
    1: Invalid input type
    2: Points array is empty
    3: Points array has invalid shape
    4: Points contain negative coordinates
    5: Points exceed image dimensions
    """
    # Error handling for input type
    if not isinstance(points, (list, np.ndarray)):
        if error_codes:
            return None, "Error 1: Input must be a list or numpy array. Got type: " + str(type(points))
        else:
            raise TypeError("Input must be a list or numpy array")
    
    # Convert to numpy array if it's a list
    if isinstance(points, list):
        try:
            points = np.array(points)
        except:
            if error_codes:
                return None, "Error 1: Could not convert list to numpy array"
            else:
                raise ValueError("Could not convert list to numpy array")
    
    # Check if points array is empty
    if points.size == 0:
        if error_codes:
            return None, "Error 2: Points array is empty"
        else:
            raise ValueError("Points array is empty")
    
    # Check points shape
    if points.ndim != 2 or points.shape[1] != 2:
        if error_codes:
            return None, f"Error 3: Points must have shape (n,2). Got shape: {points.shape}"
        else:
            raise ValueError(f"Points must have shape (n,2). Got shape: {points.shape}")
    
    # Check for negative coordinates
    if np.any(points < 0):
        if error_codes:
            return None, "Error 4: Points contain negative coordinates"
        else:
            raise ValueError("Points contain negative coordinates")

    # Check if points exceed image dimension
    width = int(np.max(points[:, 0])) + 1
    height = int(np.max(points[:, 1])) + 1
    if np.any(points[:, 0] >= width) or np.any(points[:, 1] >= height):
        if error_codes:
            return None, f"Error 5: Points exceed image dimensions ({width}x{height})"
        else:
            raise ValueError(f"Points exceed image dimensions ({width}x{height})")
    
    image = np.zeros(shape, dtype=np.uint8)
    cv2.fillPoly(
        image,
        [points],
        color = (255)
        )
    return image
