import torch
from torch.utils.data import DataLoader
from model import CNNNetwork
from dataset import CryDataset
from train import mel_spectrogram

from audio_utils import CLASS_MAPPING, NUM_CLASSES


def predict(model, input, target, CLASS_MAPPING):
    model.eval()
    with torch.no_grad():
        predictions = model(input)
        predicted_index = predictions[0].argmax(0)
        if predicted_index < 0 or predicted_index >= NUM_CLASSES:
            print("Predicted index is out of range.")
            return None
        predicted = CLASS_MAPPING[predicted_index]
        expected = CLASS_MAPPING[target]
    return predicted, expected


if __name__ == "__main__":
    # load back the model
    cnn = CNNNetwork()
    state_dict = torch.load("cnnnet.pth")
    cnn.load_state_dict(state_dict)

    ds = CryDataset(mel_spectrogram, device="cpu", audio_dir='clean')

    batch_size = 1  # Set the batch size to 1 for one sample at a time
    data_loader = DataLoader(ds, batch_size=batch_size, shuffle=False)

    for batch in data_loader:
        # Unpack the batch
        inputs, targets = batch

        # Make inferences for each sample in the batch
        for i in range(len(inputs)):
            input = inputs[i].unsqueeze(0)  # Reshape the input for inference
            predicted, expected = predict(
                cnn, input, targets[i], CLASS_MAPPING)
            print(f"Predicted: '{predicted}', Expected: '{expected}'")
