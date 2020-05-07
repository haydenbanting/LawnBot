import numpy as np


def magnitude_spectrum(image):

    #2D frequency spectrum
    f = np.fft.fft2(image)

    #shift 0-frequency componenet to center
    f_shift = np.fft.fftshift(f)

    return 20*np.log(np.abs(f_shift))