from importlib import resources
import os

# Paths
datasets_dir = resources.files("myosotis_researches").joinpath("CcGAN", "datasets")


# Function
def uninstall_datasets():
    if os.path.exists(datasets_dir):
        os.rmdir(datasets_dir)


__all__ = ["uninstall_datasets"]
