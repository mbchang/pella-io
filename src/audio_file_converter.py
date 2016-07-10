from __future__ import print_function
import numpy as np
import os
import pprint
import librosa
import matplotlib.pyplot as plt
from audio_models import BeatInterval
print('#'*180)

print(os.path.abspath(librosa.__file__))

# load audio file
audio_path = librosa.util.example_audio_file()
audio_path = '../src/audio/medium.m4a'
# audio_path = '../audio/.mp3'
y, sr = librosa.load(audio_path)
y_mono = librosa.to_mono(y)
print('y', y.shape)
print('sr', sr)
print('y_mono', y_mono.shape)
# assert(False)

# mel spectrogram
def mel_spetrogram(y, sr):
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
    log_S = librosa.logamplitude(S, ref_power=np.max)
    print('spectrogram', S.shape)

    plt.figure(figsize=(12,4))
    librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
    plt.title('mel power spectrogram')
    plt.colorbar(format='%+02.0f dB')
    plt.tight_layout()
    plt.savefig('mel power spectrogram.png')
    return log_S


# 1 Separate harmonics and percussive
def harmonics_and_percussive(y, sr):
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    S_harmonic   = librosa.feature.melspectrogram(y_harmonic, sr=sr)
    S_percussive = librosa.feature.melspectrogram(y_percussive, sr=sr)
    log_Sh = librosa.logamplitude(S_harmonic, ref_power=np.max)
    log_Sp = librosa.logamplitude(S_percussive, ref_power=np.max)
    print('y_harmonic', y_harmonic.shape)
    print('y_percussive', y_percussive.shape)

    plt.figure(figsize=(12,6))
    plt.subplot(2,1,1)
    librosa.display.specshow(log_Sh, sr=sr, y_axis='mel')
    plt.title('mel power spectrogram (Harmonic)')
    plt.colorbar(format='%+02.0f dB')
    plt.subplot(2,1,2)
    librosa.display.specshow(log_Sp, sr=sr, x_axis='time', y_axis='mel')
    plt.title('mel power spectrogram (Percussive)')
    plt.colorbar(format='%+02.0f dB')
    plt.tight_layout()
    # plt.show() -- if you have matplotlib.pyplot
    plt.savefig('harmonics and percussive.png')
    return y_harmonic, y_percussive

# pitch values
def chromagram(y_harmonic, sr):
    C = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
    print('chromagram', C.shape)

    plt.figure(figsize=(12,4))
    librosa.display.specshow(C, sr=sr, x_axis='time', y_axis='chroma', vmin=0, vmax=1)
    plt.title('chromagram')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig('chromagram.png')
    return C

# mel frequency cepstral coefficients
def mfcc(log_S, n_mfcc=13, show=False):
    mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=13)

    delta_mfcc  = librosa.feature.delta(mfcc)
    delta2_mfcc = librosa.feature.delta(mfcc, order=2)

    if show == True:
        plt.figure(figsize=(12, 6))
        plt.subplot(3,1,1)
        librosa.display.specshow(mfcc)
        plt.ylabel('MFCC')
        plt.colorbar()
        plt.subplot(3,1,2)
        librosa.display.specshow(delta_mfcc)
        plt.ylabel('MFCC-$\Delta$')
        plt.colorbar()
        plt.subplot(3,1,3)
        librosa.display.specshow(delta2_mfcc, sr=sr, x_axis='time')
        plt.ylabel('MFCC-$\Delta^2$')
        plt.colorbar()
        plt.tight_layout()
        plt.savefig('mfcc.png')

    # For future use, we'll stack these together into one matrix
    M = np.vstack([mfcc, delta_mfcc, delta2_mfcc])

    return delta_mfcc, delta2_mfcc, M

def feature_sync(M, beats, show=False):
    M_sync = librosa.feature.sync(M, beats)

    if show == True:
        plt.figure(figsize=(12,6))
        plt.subplot(2,1,1)
        librosa.display.specshow(M)
        plt.title('MFCC-$\Delta$-$\Delta^2$')
        plt.yticks(np.arange(0, M.shape[0], 13), ['MFCC', '$\Delta$', '$\Delta^2$'])
        plt.colorbar()
        plt.subplot(2,1,2)
        librosa.display.specshow(M_sync)
        librosa.display.time_ticks(librosa.frames_to_time(beats, sr=sr))
        plt.yticks(np.arange(0, M_sync.shape[0], 13), ['MFCC', '$\Delta$', '$\Delta^2$'])
        plt.title('Beat-synchronous MFCC-$\Delta$-$\Delta^2$')
        plt.colorbar()
        plt.tight_layout()
        plt.savefig('feature_sync.png')

    return M_sync

def chroma_sync(C, beats, aggregate=np.median, show=True):
    C_sync = librosa.feature.sync(C, beats, aggregate=np.median)
    print('C_sync', C_sync.shape)

    if show == True:
        plt.figure(figsize=(12,24))
        plt.subplot(2, 1, 1)
        librosa.display.specshow(C, sr=sr, y_axis='chroma', vmin=0.0, vmax=1.0, x_axis='time')
        plt.title('Chroma')
        plt.colorbar()
        plt.subplot(2, 1, 2)
        librosa.display.specshow(C_sync, y_axis='chroma', vmin=0.0, vmax=1.0)
        beat_times = librosa.frames_to_time(beats, sr=sr)
        librosa.display.time_ticks(beat_times)
        plt.title('Beat-synchronous Chroma (median aggregation)')
        plt.colorbar()
        plt.tight_layout()
        plt.savefig('chroma_sync.png')
    return C_sync

# get notes
# output: (timesteps, notes)
def get_notes(cgram, threshold):
    cgramT = np.transpose(cgram)
    for row in cgramT:
        #top3 = row.argsort()[-3:][::-1]
        #row = np.zeros(len(row))
        #row[top3] = 1
        row[row > threshold] = 1
        row[row <= threshold] = 0

    return cgramT

def decompose(y, n_components=8):
    # How about something more advanced?  Let's decompose a spectrogram with NMF, and then resynthesize an individual component
    D = librosa.stft(y)

    # Separate the magnitude and phase
    S, phase = librosa.magphase(D)

    # Decompose by nmf
    components, activations = librosa.decompose.decompose(S, n_components, sort=True)

    plt.figure(figsize=(12,4))

    plt.subplot(1,2,1)
    librosa.display.specshow(librosa.logamplitude(components**2.0, ref_power=np.max), y_axis='log')
    plt.xlabel('Component')
    plt.ylabel('Frequency')
    plt.title('Components')

    plt.subplot(1,2,2)
    librosa.display.specshow(activations)
    plt.xlabel('Time')
    plt.ylabel('Component')
    plt.title('Activations')

    plt.tight_layout()
    plt.savefig('components_activations.png')

    print('components', components.shape)
    print('activations', activations.shape)
    return components, activations, phase

def reconstruct(components, activations, phase):
    # Play back the reconstruction
    # Reconstruct a spectrogram by the outer product of component k and its activation
    D_k = components.dot(activations)

    # invert the stft after putting the phase back in
    y_k = librosa.istft(D_k * phase)
    return y_k

# is there a way to get the frequency range?
def get_freq_component(y, k=4):
    components, activations, phase = decompose(y)
    D_k = np.multiply.outer(components[:, k], activations[k])

    # invert the stft after putting the phase back in
    y_k = librosa.istft(D_k * phase)
    return y_k

def beat_track(y_percussive, sr, log_S):
    # Now, let's run the beat tracker.
    # We'll use the percussive component for this part
    plt.figure(figsize=(12, 6))
    tempo, beats = librosa.beat.beat_track(y=y_percussive, sr=sr)

    # Let's re-draw the spectrogram, but this time, overlay the detected beats
    plt.figure(figsize=(12,4))
    librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')

    # Let's draw transparent lines over the beat frames
    plt.vlines(beats, 0, log_S.shape[0], colors='r', linestyles='-', linewidth=2, alpha=0.5)
    plt.axis('tight')
    plt.colorbar(format='%+02.0f dB')
    plt.tight_layout()
    return tempo, beats

# input: binary mask (timestamps, num_notes)
# TODO: chromagram to audio timeseries
def notes2mp3():
    # 1 convert it back to frequency/spectrogram
    # 2 save
    pass

# index freq_map. assume we start at c1
def notes2freq(notes):
    # notes (num_notes, timesteps); may not be onehot
    # map: (num_notes)
    # output: (timesteps)
    freqs = []
    timesteps, num_freqs  = notes.shape
    print('notes', notes.shape)
    assert num_freqs%12 == 0
    freq_map = getFreqMap(num_freqs/12)
    for t in range(timesteps):
        freq_tmp = freq_map[notes[t] > 0]
        if len(freq_tmp) == 0:
            freq_tmp = np.array([0])
        print(freq_tmp)
        freqs.append(freq_tmp)
    print('freqs', freqs)
    return freqs

# assume we start at c1
def getFreqMap(num_octaves):
    freqMap = np.zeros(num_octaves*12)
    freqMap[0:12] = [8.1757989156, 8.6619572180, 9.1770239974, 9.7227182413, 10.3008611535, 10.9133822323, 11.5623257097, 12.2498573744, 12.9782717994, 13.7500000000, 14.5676175474, 15.4338531643]
    freqMap = freqMap * 4
    for i in range(1, num_octaves - 1):
        lo = 12 * (i - 1)
        med = 12 * i
        hi = 12 * (i + 1)
        print(lo, med, hi)
        freqMap[med : hi] = freqMap[lo : med] * 2

    return freqMap

def getBeatIntervalsFromNotes(notes_mask, beats):
    freqs = notes2freq(notes_mask)  # (timesteps, num_freqs) list
    beats = [0]+beats  # (num_beats), not necessarily timesteps
    timesteps = len(freqs)

    beatIntervals = []
    for i in range(timesteps):
        print(freqs[i])
        lowest_freq = min(freqs[i])
        frequencies = freqs[i]
        mults = [1 for i in frequencies]
        nextBeatInterval = BeatInterval(lowest_freq, frequencies, mults)
        beatIntervals.append(nextBeatInterval)
    return beatIntervals


def getTwinkle():
    log_S = mel_spetrogram(y, sr)
    y_harmonic, y_percussive = harmonics_and_percussive(y, sr)
    cgram = chromagram(y_harmonic, sr)
    tempo, beats = beat_track(y_percussive, sr, log_S)
    # components, activaions = decompose(y)

    delta_mfcc, delta2_mfcc, M = mfcc(log_S)
    chroma_sync_gram = chroma_sync(cgram, beats)
    notes = get_notes(chroma_sync_gram, 0.5)
    # print(notes.shape)
    freqs = notes2freq(notes)

    beatIntervals = getBeatIntervalsFromNotes(notes, beats)
    # for_tejas = (freqs, beats)
    
    print('beats',beats.shape)
    # res = np.array([beats, notes])
    res = np.array([beats, notes])
    print(res)
    return beatIntervals

getTwinkle()
