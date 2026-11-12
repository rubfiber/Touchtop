import math

import Network
import numpy as np
from collections import deque
from numpy.fft import rfft as dft # discrete fourier transform
from numpy.fft import rfftfreq

rate = 16000
silence_threshold = 0.01
def frame_features(tilt, frame):
    amplitude = np.sqrt(np.mean(frame ** 2))
    if amplitude < silence_threshold: #silence
        frequency = 0
    else:
        spectrum = np.abs(dft(frame*np.hanning(len(frame))))
        frequencies = rfftfreq(len(frame), 1/ rate)
        frequency = frequencies[np.argmax(spectrum[1:]) + 1]

    return [frequency, amplitude, tilt]

