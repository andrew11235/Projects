# https://towardsdatascience.com/handwritten-digit-mnist-pytorch-977b5338e627

import torch
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
import torch.nn.functional as F
from torch import nn, optim


def load_data():
    train_set = datasets.MNIST('../', download=True, train=True, transform=transforms.ToTensor())
    val_set = datasets.MNIST('../', download=True, train=False, transform=transforms.ToTensor())

    train_dl = torch.utils.data.DataLoader(train_set, batch_size=64, shuffle=True)
    val_dl = torch.utils.data.DataLoader(val_set, batch_size=64, shuffle=True)

    return train_dl, val_dl


def main():
    input_dims = 28 * 28
    hidden_dims = [128, 64]
    output_dims = 10
    
    model = nn.Sequential
    
    train_dl, val_dl = load_data()
    for images, label in train_dl:
        for i in range(3):
            plt.imshow(images[i].numpy().squeeze(), cmap='gray')
            plt.show()
        break


if __name__ == '__main__':
    main()
