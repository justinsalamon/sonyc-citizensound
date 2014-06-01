#!/usr/bin/env python
from pylab import *
import wave
import numpy as np
from scipy import signal
import sys

audiofile = sys.argv[1]

#load audio file
waveFile = wave.open(audiofile, 'r')

#get length
length = waveFile.getnframes()

#get sample rate
fs = waveFile.getframerate()

#get block size
blocksize = waveFile.getsampwidth()

#read audio byte array as string
data = waveFile.readframes(length)

#convert from string array to numeric 16 bit byte array
vals = np.fromstring(data, dtype='h')

#convert to float with range -1 to +1
floats = vals/32768.0

NFFT = 1024       # the length of the windowing segments
Fs = fs  # the sampling frequency

# Pxx is the segments x freqs array of instantaneous power, freqs is
# the frequency vector, bins are the centers of the time bins in which
# the power is computed, and im is the matplotlib.image.AxesImage
# instance
cmap = plt.cm.jet
Pxx, freqs, bins, im = specgram(floats, NFFT=NFFT, Fs=Fs, noverlap=900,cmap=cmap)
show()