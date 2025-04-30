from importlib import resources
import os

datasets_dir = resources.files("myosotis_researches").joinpath("CcGAN", "datasets")


def show_datasets():

    if not os.path.exists(datasets_dir):
        os.makedirs(datasets_dir, exist_ok=True)

    datasets = []
    for item in os.listdir(datasets_dir):
        datasets.append(item)
    print("\n".join(datasets))
