import matplotlib.pyplot as plt
import os
import torchaudio

# Load the raw audio file
raw_wav, sr = torchaudio.load(os.path.join(
    os.path.dirname(__file__), 'raw', 'Silence', 'silence.wav_1.wav'))

# Create a MelSpectrogram transform
mel_transform = torchaudio.transforms.MelSpectrogram(
    win_length=int(0.03 * sr),
    hop_length=int(0.01 * sr),
    n_mels=64,
    n_fft=int(0.03 * sr)
)

# Apply the transform to the raw audio
mel_spectrogram = mel_transform(raw_wav)

# Convert to decibels
mel_spectrogram_db = torchaudio.transforms.AmplitudeToDB()(mel_spectrogram)

# Plot the Mel spectrogram
plt.figure(figsize=(12, 4))
plt.imshow(mel_spectrogram_db[0].numpy(),
           cmap='viridis', aspect='auto', origin='lower')
plt.title('Mel Spectrogram')
plt.xlabel('Time')
plt.ylabel('Mel Filter')
plt.colorbar(format='%+2.0f dB')
plt.show()
