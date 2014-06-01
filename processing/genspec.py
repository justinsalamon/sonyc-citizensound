# CREATED: 5/31/14 4:27 PM by Justin Salamon <justin.salamon@nyu.edu>

import argparse, os
import essentia.standard as estd
import numpy as np
import pylab as pl
# import audiolab

FS = 44100
WINDOWTYPE = 'hann'
FRAMESIZE = 1024
HOPSIZE = FRAMESIZE / 4

def genspec(filename):

    loader = estd.MonoLoader(filename = filename,
                            downmix = 'mix',
                            sampleRate = FS)
    win = estd.Windowing(type = WINDOWTYPE)
    spectrum = estd.Spectrum()

    audio = loader()
    spec = []
    for frame in estd.FrameGenerator(audio, FRAMESIZE, HOPSIZE):
        spec.append(spectrum(win(frame)))

    spec = np.asarray(spec)
    spec = np.flipud(spec.T)
    dbspec = 20*np.log10(spec)

    # PLOTTING CODE
    w = 9
    h = 2
    fig = pl.figure(frameon=False)
    fig.set_size_inches(w,h)
    ax = pl.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    pl.imshow(dbspec, aspect='normal', cmap='hot')

    # SAVE TO DISK
    pngfile = os.path.splitext(filename)[0] + ".png"
    fig.savefig(pngfile, dpi=100)
    # pl.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate dataset")
    parser.add_argument("filename", help="Path to file with reference/estimate file pairs")
    # parser.add_argument("outputfile", help="Desired path to output file with results")
    # parser.add_argument("hop", help="Desired hop size (in seconds) for the comparison")

    args = parser.parse_args()
    if args.filename is not None:
        genspec(args.filename)