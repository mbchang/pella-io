from __future__ import print_function
import numpy as np
import librosa
import matplotlib.pyplot as plt
print('#'*180)

# load audio file
audio_path = librosa.util.example_audio_file()
audio_path = '../audio/twinkle_twinkle.mp3'
y, sr = librosa.load(audio_path)
y_mono = librosa.to_mono(y)
print('y', y.shape)
print('sr', sr)
print('y_mono', y_mono.shape)

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

# get notes
# output: (timesteps, notes)
def get_notes(cgram):
    pass

def mfcc():
    # Next, we'll extract the top 13 Mel-frequency cepstral coefficients (MFCCs)
    mfcc        = librosa.feature.mfcc(S=log_S, n_mfcc=13)

    # Let's pad on the first and second deltas while we're at it
    delta_mfcc  = librosa.feature.delta(mfcc)
    delta2_mfcc = librosa.feature.delta(mfcc, order=2)

    # How do they look?  We'll show each in its own subplot
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

    # For future use, we'll stack these together into one matrix
    M = np.vstack([mfcc, delta_mfcc, delta2_mfcc])
    return M

def decompose(y):
    # How about something more advanced?  Let's decompose a spectrogram with NMF, and then resynthesize an individual component
    D = librosa.stft(y)

    # Separate the magnitude and phase
    S, phase = librosa.magphase(D)

    # Decompose by nmf
    components, activations = librosa.decompose.decompose(S, n_components=8, sort=True)

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

    return components, activations

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

if __name__=="__main__":
    log_S = mel_spetrogram(y, sr)
    y_harmonic, y_percussive = harmonics_and_percussive(y, sr)
    cgram = chromagram(y_harmonic, sr)
    tempo, beats = beat_track(y_percussive, sr, log_S)
    components, activaions = decompose(y)
