import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim


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


# SSIM


def _SSIM(image_1, image_2):

    array_1 = np.array(image_1)
    array_2 = np.array(image_2)
    score, _ = ssim(array_1, array_2, channel_axis=-1, full=True)
    return score


def SSIM(images):
    SSIM_sum = 0
    n = len(images)
    for i in range(n):
        for j in range(i + 1, n):
            SSIM_sum += _SSIM(images[i], images[j])
    return SSIM_sum / (n * (n - 1) / 2)


# Similarity
_method_dict = {"MSE": MSE, "SSIM": SSIM}


def similarity(images, method):
    return _method_dict[method](images)


__all__ = ["similarity"]
