import torchaudio
import torch
from tqdm import tqdm
from dataset import CryDataset
from torch.utils.data import DataLoader
from model import CNNNetwork
from torch import nn


from audio_utils import BATCH_SIZE, EPOCHS, LEARNING_RATE, N_MELS, SAMPLE_RATE


def create_data_loader(train_data, batch_size):
    train_dataloader = DataLoader(train_data, batch_size=batch_size)
    return train_dataloader


def train_single_epoch(model, data_loader, loss_fn, optimiser, device):
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    for input, target in tqdm(data_loader):
        input, target = input.to(device), target.to(device)

        # calculate loss
        prediction = model(input)
        loss = loss_fn(prediction, target)

        # backpropagate error and update weights
        optimiser.zero_grad()
        loss.backward()
        optimiser.step()
        # Calculate accuracy
        _, predicted = torch.max(prediction, 1)
        total += target.size(0)
        correct += (predicted == target).sum().item()

        total_loss += loss.item()

    # Calculate accuracy
    accuracy = 100 * correct / total
    average_loss = total_loss / len(data_loader)

    print(f"Loss: {average_loss:.4f}, Accuracy: {accuracy:.2f}%")


def train(model, data_loader, loss_fn, optimiser, device, epochs):
    for i in range(epochs):
        print(f"Epoch {i+1}")
        train_single_epoch(model, data_loader, loss_fn, optimiser, device)
        print("---------------------------")
    print("Finished training")


mel_spectrogram = torchaudio.transforms.MelSpectrogram(
    sample_rate=SAMPLE_RATE,
    n_fft=512,
    hop_length=150,
    win_length=400,
    n_mels=N_MELS
)

if __name__ == "__main__":
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    print(f"Using {device}")

    # instantiating our dataset object and create data loader

    ds = CryDataset(mel_spectrogram, device, audio_dir='clean')
    train_dataloader = create_data_loader(ds, BATCH_SIZE)

    # construct model and assign it to device
    cnn = CNNNetwork().to(device)
    # print(cnn)

    # initialise loss funtion + optimiser
    loss_fn = nn.CrossEntropyLoss()
    optimiser = torch.optim.Adam(cnn.parameters(),
                                 lr=LEARNING_RATE)

    # train model
    train(cnn, train_dataloader, loss_fn, optimiser, device, EPOCHS)

    # save model
    torch.save(cnn.state_dict(), "cnnnet.pth")
    print("Trained feed forward net saved at cnnnet.pth")
