import numpy as np
from scipy.fftpack import dct, idct

# DCT 2D
def dct_2d(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# IDCT 2D
def idct_2d(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')