import numpy as np
import torch
from torch import nn, optim
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
from PIL import Image


def load_data(batch_size):
    train_set = datasets.MNIST('../', download=True, train=True, transform=transforms.ToTensor())
    val_set = datasets.MNIST('../', download=True, train=False, transform=transforms.ToTensor())

    train_dl = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_dl = torch.utils.data.DataLoader(val_set, batch_size=batch_size, shuffle=True)

    return train_dl, val_dl


def load_custom(path):
    img = Image.open(path)
    plt.imshow(img, cmap='gray_r')
    plt.show()

    transform = transforms.ToTensor()
    custom = transform(img)
    custom_dl = torch.utils.data.DataLoader(custom)

    return custom_dl


def train(epochs, model, train_dl, optimizer, criterion):
    for e in range(epochs):
        total_loss = 0
        for images, labels in train_dl:
            images = images.view(images.shape[0], -1)

            optimizer.zero_grad()

            output = model(images)
            loss = criterion(output, labels)

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {e + 1}, Loss: {total_loss / len(train_dl)}")

    return model


def evaluate(model, val_dl, metric=False):
    correct_count, all_count = 0, 0
    for images, labels in val_dl:
        for i in range(len(labels)):
            img = images[i].view(1, 784)

            with torch.no_grad():
                log_probs = model(img)

            ps = torch.exp(log_probs)
            prob = list(ps.numpy()[0])

            pred_label = prob.index(max(prob))
            true_label = labels.numpy()[i]

            if true_label == pred_label:
                correct_count += 1
            elif metric:
                plt.imshow(images[i].numpy().reshape((28, 28)), cmap='gray')
                plt.show()
                print(f'Predicted: {pred_label}, Actual: {true_label}')
                input()
                plt.close('all')

            all_count += 1

    print(f'Accuracy: {correct_count / all_count}')


def evaluate_custom(model, custom):
    for image in custom:
        img_in = image.view(1, 784)

        with torch.no_grad():
            log_probs = model(img_in)

        ps = torch.exp(log_probs)
        prob = list(ps.numpy()[0])

        pred_label = prob.index(max(prob))

        print(f'Predicted: {pred_label}')
        break

def main():
    batch_size = 64
    train_dl, val_dl = load_data(batch_size)

    input_dims = 28 * 28
    ly1_dims = 128
    ly2_dims = 64
    output_dims = 10

    try:
        model = torch.load('./mnist_model.pt')
    except FileNotFoundError:
        model = nn.Sequential(nn.Linear(input_dims, ly1_dims), nn.ReLU(),
                              nn.Linear(ly1_dims, ly2_dims), nn.ReLU(),
                              nn.Linear(ly2_dims, output_dims), nn.LogSoftmax(dim=1))

    alpha = 0.00005
    gamma = 0.5
    optimizer = optim.SGD(model.parameters(), lr=alpha, momentum=gamma)
    criterion = nn.NLLLoss()

    # model = train(3, model, train_dl, optimizer, criterion)
    # torch.save(model, './mnist_model.pt')

    evaluate(model, val_dl, metric=True)

    # custom = load_custom('./custom/custom8.png')
    # evaluate_custom(model, custom)


if __name__ == '__main__':
    main()
