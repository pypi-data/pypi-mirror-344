import numpy as np
from PIL import Image


# MSE
def _MSE(image_1, image_2):
    array_1 = np.array(image_1) / 255
    array_2 = np.array(image_2) / 255
    n, m, _ = array_1.shape
    return np.sum((array_1 - array_2) ** 2) / (n * m * 3)


def MSE(images):
    MSE_sum = 0
    n = len(images)
    for i in range(n):
        for j in range(i + 1, n):
            MSE_sum += _MSE(images[i], images[j])
    return MSE_sum / (n * (n - 1) / 2)


# Similarity
_method_dict = {"MSE": MSE}


def similarity(images, method):
    return _method_dict[method](images)


__all__ = ["similarity"]
