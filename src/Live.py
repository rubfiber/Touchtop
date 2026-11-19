import collections
import sys
import threading
import time

from torch import Value
from math import sqrt
import numpy as np, serial, sounddevice as sd

from numpy.fft import rfft as dft # discrete fourier transform
from numpy.fft import rfftfreq

import platform

rate = 16000
silence_threshold = 0.01
sequence_length = 28
def frame_features(tilt, frame):
    amplitude = np.sqrt(np.mean(frame ** 2))
    if amplitude < silence_threshold: #silence
        frequency = 0
    else:
        spectrum = np.abs(dft(frame*np.hanning(len(frame))))
        frequencies = rfftfreq(len(frame), 1/ rate)
        frequency = frequencies[np.argmax(spectrum[1:]) + 1]

    return [frequency, amplitude, tilt]

if platform.system() != "Windows":
    default_port = "/dev/TTYUSB0" # depends on os and board
else:
    default_port = "COM3"
# if not any of these then check

if len(sys.argv) > 1:
    default_port = sys.argv[1] # default port is 1st command line argument

SR, BLOCK, SEQ_LEN, POST = 16000, 512, 28, 0.6
class Recorder:

    def __init__(self, port=default_port, baud=115200):
        self.MPU = collections.deque(maxlen=4000)      # (t, ax, ay, az) # history
        self.audio = collections.deque(maxlen=400)     # (t, block)
        self.ser = serial.Serial(port, baud, timeout=1)
        threading.Thread(target=self.arduino_in(), daemon=True).start()
        self.stream = sd.InputStream(samplerate=SR, blocksize=BLOCK,
                                     channels=1, callback=self.on_audio) #audio recording
        self.stream.start()

    def arduino_in(self): # get loop from serial
        while True:
            read_line = self.ser.readline().decode(errors='ignore').strip() # spit words
            try:
                v = [float(s) for s in read_line.split(",")]
            except ValueError: continue

            if len(v) >= 3:
                self.MPU.append((time.perf_counter() , *v[:3]))

    def on_audio(self, data):
        self.audio.append((time.perf_counter(), data[:, 0].copy()))

    def window(self, t_end): # get all timestamp and audio buffer pairs and gets last seq length pairs
        blocks = [
            (t, b)
            for t, b in self.audio if t<=t.end
        ][-sequence_length:]
        mpu = np.array(self.MPU)
        if len(blocks) < sequence_length or len(mpu) < 2: # if less than seq length blocks exist then don't do anything
            return None

        feats = []
        for t, b in blocks: # time audio buffer - same as frame features function
            amplitude = sqrt(np.mean(b) ** 2)
            spectrum = np.abs(dft(b * np.hanning(len(b))))
            frequencies = rfftfreq(len(b), 1 / rate)
            frequency = frequencies[np.argmax(spectrum[1:]) + 1]
            pitch, roll, yaw = (np.interp(t, mpu[:, 0], mpu[:, i]) for i in (1, 2, 3))
            feats.append([frequency, amplitude, pitch, roll, yaw])

        return np.array(feats, dtype=np.float32)

    def on_close(self):
        self.ser.close()


recorder = Recorder(port=default_port)



