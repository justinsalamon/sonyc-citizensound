# CREATED: 5/31/14 4:27 PM by Justin Salamon <justin.salamon@nyu.edu>

import argparse, os, glob, json
import essentia.standard as estd
import numpy as np
import pylab as pl
# import audiolab

FS = 44100
WINDOWTYPE = 'hann'
FRAMESIZE = 1024
HOPSIZE = FRAMESIZE / 4


def genspecfolder(audiofolder, specfolder, jsonfolder):

    files = glob.glob(os.path.join(audiofolder, "*.wav"))
    sounds = []

    for f in files:
        pngfile = os.path.split(f)[1][:-3] + 'png'
        pngfile = os.path.join(specfolder,pngfile)
        print pngfile
        duration = genspec(f, pngfile)
        metadata = {}
        metadata['duration'] = duration
        metadata['filename'] = os.path.split(f)[1][:-4]
        sounds.append(metadata)

    clips = {}
    clips['sounds'] = sounds
    jsonfile = os.path.join(jsonfolder, "clips.json")
    j = json.dumps(clips, indent=4)
    with open(jsonfile, 'w') as f:
        print >> f, j
        f.close()


def genspec(audiofile, specfile):

    loader = estd.MonoLoader(filename = audiofile,
                            downmix = 'mix',
                            sampleRate = FS)
    win = estd.Windowing(type = WINDOWTYPE)
    spectrum = estd.Spectrum()

    audio = loader()
    duration = len(audio) / float(FS)
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
    pl.imshow(dbspec, aspect='normal', cmap='jet')

    # SAVE TO DISK
    # pngfile = os.path.splitext(filename)[0] + ".png"
    fig.savefig(specfile, dpi=100)
    # pl.show()

    return duration


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate spectrograms and json file")
    parser.add_argument("audiofolder", help="Path to folder with audio files to process")
    parser.add_argument("specfolder", help="Path to folder to save spectrograms")
    parser.add_argument("jsonfolder", help="Path to folder to json file")

    args = parser.parse_args()
    if args.audiofolder is not None:
        genspecfolder(args.audiofolder, args.specfolder, args.jsonfolder)
