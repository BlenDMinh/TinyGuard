RAW = 'raw'
CLEAN = 'clean'
SAMPLE_RATE = 16000
THRESHOLD = 0
DELTA_TIME = 5
CLASS_MAPPING = [
    "Cat",
    "ChurchBell",
    "Cry",
    "Dog",
    "Laugh",
    "Rain",
    "Silence",
    "WaterDrop",
    "Wind"
]
BATCH_SIZE = 60
EPOCHS = 30
LEARNING_RATE = 0.0001
N_MELS = 64
NFFT = 1024
HOP_LEN = int(2*(10**-3)*SAMPLE_RATE)
WIN_LEN = int(5*(10**-3)*SAMPLE_RATE)
NUM_CLASSES = len(CLASS_MAPPING)
