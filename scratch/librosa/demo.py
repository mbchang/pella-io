from __future__ import print_function
import numpy as np
import librosa
import matplotlib.pyplot as plt
print('#'*180)

# load audio file
audio_path = librosa.util.example_audio_file()
audio_path = '../audio/Africa.mp3'
y, sr = librosa.load(audio_path)

# mel spectrogram
def mel_spetrogram(y, sr):
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
    log_S = librosa.logamplitude(S, ref_power=np.max)

    plt.figure(figsize=(12,4))
    librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
    plt.title('mel power spectrogram')
    plt.colorbar(format='%+02.0f dB')
    plt.tight_layout()
    plt.savefig('mel power spectrogram.png')


# 1 Separate harmonics and percussive
def harmonics_and_percussive(y, sr):
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    S_harmonic   = librosa.feature.melspectrogram(y_harmonic, sr=sr)
    S_percussive = librosa.feature.melspectrogram(y_percussive, sr=sr)
    log_Sh = librosa.logamplitude(S_harmonic, ref_power=np.max)
    log_Sp = librosa.logamplitude(S_percussive, ref_power=np.max)

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
    plt.savefig('harmonics and percussive.png')
    return y_harmonic, y_percussive

# 2 Chromagram: Pitch values
def chromagram(y_harmonic, sr):
    C = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)

    plt.figure(figsize=(12,4))
    librosa.display.specshow(C, sr=sr, x_axis='time', y_axis='chroma', vmin=0, vmax=1)
    plt.title('Chromagram')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig('Chromagram.png')

y_harmonic, y_percussive = harmonics_and_percussive(y, sr)
chromagram(y_harmonic, sr)
