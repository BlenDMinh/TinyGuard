# config = {
#     "DATA_PATH": "./dataset/src/",
#     "CLASS_NUM": 2,
#     "BOX_NUM_PER_CELL": 2,
#     "STRIDE": 7,
# }

config = dict(
    image_data_csv = "./image_data.csv",
    image_data_path = "./dataset/src/",
    audio_data_csv = "./audio_data.csv",
    audio_data_path = "./dataset/clean/",
    class_num = 2,
    box_num = 2,
    stride = 7,
    audio_data_factor = 0.7,
    data_threshold = 0.5
)