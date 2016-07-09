from __future__ import print_function
import numpy as np
import librosa
import matplotlib.pyplot as plt
print('#'*180)

# load audio file
audio_path = librosa.util.example_audio_file()
audio_path = '../audio/twinkle_twinkle.mp3'
y, sr = librosa.load(audio_path)

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
    print(C_sync)

    if show == True:
        plt.figure(figsize=(12,6)) 
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
        row[row > threshold] = 1
        row[row <= threshold] = 0
    return cgramT

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

if __name__ == "__main__":
    log_S = mel_spetrogram(y, sr)
    y_harmonic, y_percussive = harmonics_and_percussive(y, sr)
    cgram = chromagram(y_harmonic, sr)
    tempo, beats = beat_track(y_percussive, sr, log_S)
    delta_mfcc, delta2_mfcc, M = mfcc(log_S)
    chroma_sync_gram = chroma_sync(cgram, beats)
    notes = get_notes(chroma_sync_gram, 0.7)
    print(notes)
    print(beats)
    res = np.array([beats, notes])
