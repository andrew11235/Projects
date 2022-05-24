import subprocess
from os import listdir
from time import sleep
import torch
from torch import nn, optim
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
from PIL import Image


def load_data(batch_size):
    print("*** loading database ***")
    train_set = datasets.MNIST('../', download=True, train=True, transform=transforms.ToTensor())
    val_set = datasets.MNIST('../', download=True, train=False, transform=transforms.ToTensor())

    train_dl = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_dl = torch.utils.data.DataLoader(val_set, batch_size=batch_size, shuffle=True)

    return train_dl, val_dl


def load_model(path):
    print('*** loading model ***')
    model = torch.load(path)
    return model


def new_model(input_dims, ly1_dims, ly2_dims, output_dims):
    print('*** initializing model ***')
    model = nn.Sequential(nn.Linear(input_dims, ly1_dims), nn.ReLU(),
                          nn.Linear(ly1_dims, ly2_dims), nn.ReLU(),
                          nn.Linear(ly2_dims, output_dims), nn.LogSoftmax(dim=1))
    return model


def load_custom(path):
    img = Image.open(path)
    transform = transforms.ToTensor()
    custom = transform(img)
    custom_dl = torch.utils.data.DataLoader(custom)

    return custom_dl


def train(epochs, model, train_dl, optimizer, criterion):
    print('*** training ***')
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
    print('*** evaluating ***')
    correct_count, all_count = 0, 0
    for images, labels in val_dl:
        for i in range(len(labels)):
            img = images[i].view(1, 784)

            with torch.no_grad():
                log_probs = model(img)

            ps = torch.exp(log_probs)
            prob = list(ps.numpy()[0])

            confidence = max(prob)
            predicted_label = prob.index(max(prob))

            target_label = labels.numpy()[i]

            if target_label == predicted_label:
                correct_count += 1
            elif metric:
                plt.imshow(images[i].numpy().reshape((28, 28)), cmap='gray')
                print(f'Predicted: {predicted_label}, Actual: {target_label}')
                print(f'Confidence: {round(confidence, 3)}')
                plt.show()

            all_count += 1

    print(f'Accuracy: {correct_count / all_count}')


def evaluate_custom(model, custom_path):
    print(f'*** evaluating custom: {custom_path}***')
    custom_dl = load_custom(custom_path)
    image = next(iter(custom_dl))
    img_in = image.view(1, 784)

    with torch.no_grad():
        log_probs = model(img_in)

    ps = torch.exp(log_probs)
    prob = list(ps.numpy()[0])

    confidence = max(prob)
    predicted_label = prob.index(max(prob))

    print(f'Predicted: {predicted_label}')
    print(f'Confidence: {round(confidence, 3)}')

    to_img = transforms.ToPILImage()
    plt.imshow(to_img(image), cmap='gray')
    plt.show()


def main():
    # =======================================
    load, save = True, True
    load_path = './mnist_model_new.pt'
    save_path = './mnist_model_new.pt'

    # Hyperparams
    input_dims = 28 * 28
    ly1_dims = 128
    ly2_dims = 64
    output_dims = 10

    batch_size = 64
    alpha = 0.05
    gamma = 0.5
    epochs = 0

    # Model evaluation
    eval_model = False
    metric = False
    custom = True
    custom_path = r'new'
    # =======================================

    train_dl, val_dl = load_data(batch_size)

    if load:
        model = load_model(load_path)
    else:
        model = new_model(input_dims, ly1_dims, ly2_dims, output_dims)

    optimizer = optim.SGD(model.parameters(), lr=alpha, momentum=gamma)
    criterion = nn.NLLLoss()

    if epochs != 0:
        model = train(epochs, model, train_dl, optimizer, criterion)

    if save:
        torch.save(model, save_path)
    if eval_model:
        evaluate(model, val_dl, metric=metric)

    if custom:
        if custom_path == 'new':
            subprocess.Popen([r'C:\WINDOWS\system32\mspaint.exe', r'.\customTemplate.png'])
            dir_files = listdir(r'.\custom')
            while len(dir_files) == len(listdir('custom')):
                sleep(0.5)

            new_dir_files = listdir(r'.\custom')

            for f in dir_files:
                new_dir_files.remove(f)

            custom_path = rf'.\custom\{new_dir_files[0]}'

        evaluate_custom(model, custom_path)


if __name__ == '__main__':
    main()
