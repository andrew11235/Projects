import torch
from torchvision import transforms, datasets
from torch import nn, optim


def load_data(batch_size):
    train_set = datasets.MNIST('../', download=True, train=True, transform=transforms.ToTensor())
    val_set = datasets.MNIST('../', download=True, train=False, transform=transforms.ToTensor())

    train_dl = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_dl = torch.utils.data.DataLoader(val_set, batch_size=batch_size, shuffle=True)

    return train_dl, val_dl


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


def evaluate(model, val_dl):
    print(val_dl)
    exit()
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
            all_count += 1

    print(f'Accuracy: {correct_count / all_count}')


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

    model = train(3, model, train_dl, optimizer, criterion)

    evaluate(model, val_dl)

    torch.save(model, './mnist_model.pt')


if __name__ == '__main__':
    main()
