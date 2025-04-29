from importlib import resources
import os
import shutil


# Paths
datasets_dir = resources.files("myosotis_researches").joinpath("CcGAN", "datasets")


# Function
def uninstall_datasets():
    if os.path.exists(datasets_dir):
        shutil.rmtree(datasets_dir)


__all__ = ["uninstall_datasets"]
