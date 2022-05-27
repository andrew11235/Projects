import subprocess
from os import listdir
from time import sleep
import torch
from torch import nn, optim
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
from PIL import Image


def load_data(batch_size):
    """
    Loads a training set and validation set of tensors from the MNIST database
    
    :param int batch_size: the batch size to load data in
    :return: taining set (60,000 digits with target ints)
             validation set (10,000 digits with target ints)
    :rtype: torch DataLoaders
    """
    
    print("*** loading database ***")
    train_set = datasets.MNIST('../', download=True, train=True, transform=transforms.ToTensor())
    val_set = datasets.MNIST('../', download=True, train=False, transform=transforms.ToTensor())

    train_dl = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_dl = torch.utils.data.DataLoader(val_set, batch_size=batch_size, shuffle=True)

    return train_dl, val_dl


def load_model(path):
    """
    Loads a torch model from a given path 
    
    :param str path: path to load model from
    :return: torch model from path
    :rtype: torch Model
    """
    
    print('*** loading model ***')
    model = torch.load(path)
    return model


def new_model(input_dims, ly1_dims, ly2_dims, output_dims):
    """
    Returns a 4 layer model with given dimensions with ReLU
    activations and LogSoftmax probability distribution
    
    :param int input_dims: dimension of input layer
    :param int ly1_dims: dimension of first fully connected layer
    :param int ly2_dims: dimension of second fully connected layer
    :param int output_dims: dimension of output layer
    :return: newly created model with given dimensions
    :rtype: torch Model
    """
    print('*** initializing model ***')
    model = nn.Sequential(nn.Linear(input_dims, ly1_dims), nn.ReLU(),
                          nn.Linear(ly1_dims, ly2_dims), nn.ReLU(),
                          nn.Linear(ly2_dims, output_dims), nn.LogSoftmax(dim=1))
    return model


def load_custom(path):
    """
    Loads a custom image transformed as tensors
    
    :param str path: path to load image from
    :return: tensor representation of image
    :rtype: torch DataLoader
    """
    img = Image.open(path)
    transform = transforms.ToTensor()
    custom = transform(img)
    custom_dl = torch.utils.data.DataLoader(custom)

    return custom_dl


def train(epochs, model, train_dl, optimizer, criterion):
    """
    Trains the given model
    
    :param int epochs: number of epochs to train the model for
    :param Model model: the model to train
    :param Optim optimizer: optimizer used to train the model 
    :param Citic criterion: critic used to train the model
    :return: trained model
    :rtype: torch Model
    """
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
    """
    Evaluates the given model using a validation set and prints accuracy
    
    :param Model model: model to evaluate
    :param DataLoader val_dl: validation set used to evaluate model on
    :param bool metric: displays metrics of incorrectly identified digits
    """
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
    """
    Inputs a given custom image into the model
    Displays the loaded image and prediction
    
    :param Model model: torch model to evaluate on
    :param str custom_path: path of custom image
    """
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
    # ============= Parameters ==============
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

    # loads datasets
    train_dl, val_dl = load_data(batch_size)
    
    # loads or creates torch model
    if load:
        model = load_model(load_path)
    else:
        model = new_model(input_dims, ly1_dims, ly2_dims, output_dims)
        
    # initializes SGC optimizer and Negative Log Loss function
    optimizer = optim.SGD(model.parameters(), lr=alpha, momentum=gamma)
    criterion = nn.NLLLoss()
    
    # trains the model
    if epochs != 0:
        model = train(epochs, model, train_dl, optimizer, criterion)
    
    # saves model at path
    if save:
        torch.save(model, save_path)
    
    # evaluates model
    if eval_model:
        evaluate(model, val_dl, metric=metric)
    
    # evaluates new custom image or custom image from path
    if custom:
        if custom_path == 'new':
            # loads template in MS Paint
            subprocess.Popen([r'C:\WINDOWS\system32\mspaint.exe', r'.\customTemplate.png'])
            
            # detecs newly saved image and saves as custom path
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
