import csv
import torchaudio
import torch
from tqdm import tqdm
# from .dataset import CryDataset
from dataset import CryDataset
from torch.utils.data import DataLoader
# from .model import CNNNetwork
from model import CNNNetwork
from torch import nn


# from .audio_utils import BATCH_SIZE, EPOCHS, LEARNING_RATE, N_MELS, SAMPLE_RATE
from audio_utils import BATCH_SIZE, EPOCHS, LEARNING_RATE, N_MELS, SAMPLE_RATE


def create_data_loader(train_data, batch_size):
    train_dataloader = DataLoader(train_data, batch_size=batch_size)
    return train_dataloader


def step(model, data_loader, loss_fn, optimiser, device, is_train=True):
    if is_train:
        model.train()
    total_loss = 0
    correct = 0
    total = 0
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    loop = tqdm(data_loader)
    for input, target in loop:
        input, target = input.to(device), target.to(device)

        # calculate loss
        prediction = model(input)
        loss = loss_fn(prediction, target)

        if is_train:
            # backpropagate error and update weights
            optimiser.zero_grad()
            loss.backward()
            optimiser.step()

        # Calculate accuracy
        _, predicted = torch.max(prediction, 1)
        total += target.size(0)
        correct += (predicted == target).sum().item()
        
        for t, p in zip(target, predicted):
            tp += (t.item() == 0 and p.item() == 0)
            fn += (t.item() == 0 and p.item() != 0)
            tn += (t.item() != 0 and p.item() != 0)
            fp += (t.item() != 0 and p.item() == 0)
            
        total_loss += loss.item()

        loop.set_postfix(loss=loss.item(), correct=(
            predicted == target).sum().item())

    # Calculate accuracy
    accuracy = 100 * correct / total
    average_loss = total_loss / len(data_loader)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    print(f"Loss: {average_loss:.4f}, Accuracy: {accuracy:.2f}%, Precision: {precision:.2f}, Recall: {recall:.2f}")
    return average_loss, accuracy, precision, recall


def train(model, train_data_loader, test_data_loader, loss_fn, optimiser, device, epochs):
    losses = []
    accs = []
    precisions = []
    recalls = []
    test_losses = []
    test_accs = []
    test_precisions = []
    test_recalls = []
    for i in range(epochs):
        print(f"Epoch {i+1}")
        loss, acc, pre, rec = step(
            model, train_data_loader, loss_fn, optimiser, device)
        losses.append(loss)
        accs.append(acc)
        precisions.append(pre)
        recalls.append(rec)

        test_loss, test_acc, test_pre, test_rec = step(
            model, test_data_loader, loss_fn, optimiser, device, is_train=False)
        test_losses.append(test_loss)
        test_accs.append(test_acc)
        test_precisions.append(test_pre)
        test_recalls.append(test_rec)
    print("Finished training")
    return losses, accs, precisions, recalls, test_losses, test_accs, test_precisions, test_recalls


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

    train_ds = CryDataset(mel_spectrogram, device, csv_path='train_data.csv')
    test_ds = CryDataset(mel_spectrogram, device, csv_path='test_data.csv')
    train_dataloader = create_data_loader(train_ds, BATCH_SIZE)
    test_dataloader = create_data_loader(test_ds, BATCH_SIZE)

    # construct model and assign it to device
    cnn = CNNNetwork().to(device)
    # print(cnn)

    # initialise loss funtion + optimiser
    loss_fn = nn.CrossEntropyLoss()
    optimiser = torch.optim.Adam(cnn.parameters(),
                                 lr=LEARNING_RATE)

    # train model
    losses, accs, precisions, recalls, test_losses, test_accs, test_precisions, test_recalls = train(cnn, train_dataloader, test_dataloader, loss_fn,
                                                 optimiser, device, EPOCHS)

    # save model
    torch.save(cnn.state_dict(), "cnnnet.pth")
    print("Trained feed forward net saved at cnnnet.pth")
    
    with open('history.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\r')
        writer.writerows(zip(losses, accs, precisions, recalls, test_losses, test_accs, test_precisions, test_recalls))

    with open('losses.txt', 'w') as f:
        f.write(str(losses))
    with open('accuracy.txt', 'w') as f:
        f.write(str(accs))

    with open('test_losses.txt', 'w') as f:
        f.write(str(test_losses))
    with open('test_accuracy.txt', 'w') as f:
        f.write(str(test_accs))
