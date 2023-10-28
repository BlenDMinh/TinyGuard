import torchaudio
from torchaudio import transforms
waveform, sample_rate = torchaudio.load('./dataset/clean/Cry/100e2_0.wav', normalize=True)
transform = transforms.MelSpectrogram(sample_rate)
mel_specgram = transform(waveform)
print(mel_specgram.shape)