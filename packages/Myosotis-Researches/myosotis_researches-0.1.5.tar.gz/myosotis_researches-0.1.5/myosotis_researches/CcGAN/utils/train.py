import numpy as np
import torch
import matplotlib.pyplot as plt
import matplotlib as mpl


def PlotLoss(loss, filename):
    x_axis = np.arange(start=1, stop=len(loss) + 1)
    plt.switch_backend("agg")
    mpl.style.use("seaborn")
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(x_axis, np.array(loss))
    plt.xlabel("epoch")
    plt.ylabel("training loss")
    plt.legend()
    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),  shadow=True, ncol=3)
    # plt.title('Training Loss')
    plt.savefig(filename)


# compute entropy of class labels; labels is a numpy array
def compute_entropy(labels, base=None):
    value, counts = np.unique(labels, return_counts=True)
    norm_counts = counts / counts.sum()
    base = np.e if base is None else base
    return -(norm_counts * np.log(norm_counts) / np.log(base)).sum()


def predict_class_labels(net, images, batch_size=500, verbose=False, num_workers=0):
    net = net.cuda()
    net.eval()

    n = len(images)
    if batch_size > n:
        batch_size = n
    dataset_pred = IMGs_dataset(images, normalize=False)
    dataloader_pred = torch.utils.data.DataLoader(
        dataset_pred, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )

    class_labels_pred = np.zeros(n + batch_size)
    with torch.no_grad():
        nimgs_got = 0
        if verbose:
            pb = SimpleProgressBar()
        for batch_idx, batch_images in enumerate(dataloader_pred):
            batch_images = batch_images.type(torch.float).cuda()
            batch_size_curr = len(batch_images)

            outputs, _ = net(batch_images)
            _, batch_class_labels_pred = torch.max(outputs.data, 1)
            class_labels_pred[nimgs_got : (nimgs_got + batch_size_curr)] = (
                batch_class_labels_pred.detach().cpu().numpy().reshape(-1)
            )

            nimgs_got += batch_size_curr
            if verbose:
                pb.update((float(nimgs_got) / n) * 100)
        # end for batch_idx
    class_labels_pred = class_labels_pred[0:n]
    return class_labels_pred


__all__ = ["PlotLoss", "compute_entropy", "predict_class_labels"]
