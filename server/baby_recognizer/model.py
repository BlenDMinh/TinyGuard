import torch.nn as nn
import torch

model_config = [
    ('Conv', (7, 64, 2, 3)),
    'M',
    ('Conv', (3, 192, 1, 1)),
    'M',
    ('Conv', (1, 128, 1, 0)),
    ('Conv', (3, 256, 1, 1)),
    ('Conv', (1, 256, 1, 0)),
    ('Conv', (1, 512, 1, 1)),
    'M',
    (
        'MultiConv',
        [(1, 256, 1, 0), (3, 512, 1, 1)],
        4
    ),
    ('Conv', (1, 512, 1, 0)),
    ('Conv', (3, 1024, 1, 1)),
    'M',
    (
        'MultiConv',
        [(1, 512, 1, 0), (3, 1024, 1, 1)],
        2
    ),
    ('Conv', (3, 1024, 1, 1)),
    ('Conv', (3, 1024, 2, 1)),
    ('Conv', (3, 1024, 1, 1)),
    ('Conv', (3, 1024, 1, 1)),
]


class CNNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, **kwargs) -> None:
        super(CNNBlock, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, bias=False, **kwargs)
        self.batchNorm = nn.BatchNorm2d(out_channels)
        self.leakyRelu = nn.LeakyReLU(0.1)

    def forward(self, x):
        return self.leakyRelu(self.batchNorm(self.conv(x)))


class YoloV1(nn.Module):
    def __init__(self, in_channels=3, **kwargs) -> None:
        super(YoloV1, self).__init__()
        self.architecture = model_config
        self.in_channels = in_channels
        self.darknet = self._build_from_arch(self.architecture)
        self.fcs = self._build_fcs(**kwargs)

    def forward(self, x):
        x = self.darknet(x)
        return self.fcs(torch.flatten(x, start_dim=1))

    def _build_from_arch(self, architecture):
        layers = []
        in_channels = self.in_channels
        for x in self.architecture:
            if type(x) == tuple:
                archType = x[0]
                if archType == 'Conv':
                    layers.append(
                        CNNBlock(
                            in_channels, x[1][1], kernel_size=x[1][0], stride=x[1][2], padding=x[1][3])
                    )

                    in_channels = x[1][1]
                elif archType == 'MultiConv':
                    for _ in range(x[2]):
                        for conv in x[1]:
                            layers.append(
                                CNNBlock(
                                    in_channels, conv[1], kernel_size=conv[0], stride=conv[2], padding=conv[3])
                            )
                            in_channels = conv[1]
            elif type(x) == str:
                layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
        return nn.Sequential(*layers)

    def _build_fcs(self, split_size, num_boxes, num_classes):
        S, B, C = split_size, num_boxes, num_classes
        return nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024 * S * S, 496),
            nn.Dropout(0.0),
            nn.LeakyReLU(0.1),
            nn.Linear(496, S * S * (C + B * 5))
        )
