import gdown
import getpass
from importlib import resources
import os
import subprocess

# Paths
datasets_dir = resources.files("myosotis_researches").joinpath("CcGAN", "datasets")

# File ID dictionary
file_id_dict = {
    "Ra": "1CcXp7ga4Ebj7XeMA_fYH2RxTMOWvA0v5",
    "MNIST": "1SpfoZAJjQ6MvU8fm9Ant_FjJppVfTpN6",
    "Ra_sorted": "1pQ_HVkkBB7tpnaxDuStoyw_SSOS-Qqkb"
}


# Function
def install_datasets(datasets_name):

    # Makedir
    if not os.path.exists(datasets_dir):
        os.makedirs(datasets_dir, exist_ok=True)

    # Path
    zipped_dataset_path = os.path.join(datasets_dir, f"{datasets_name}_datasets.rar")

    # File ID
    file_id = file_id_dict[datasets_name]

    # URL
    url = f"https://drive.google.com/uc?id={file_id}"

    # Download
    gdown.download(url, zipped_dataset_path, quiet=False, use_cookies=False)

    # Unzip
    unzip_password = getpass.getpass("Password:")
    cmd = ["unrar", "x", f"-p{unzip_password}", zipped_dataset_path, datasets_dir]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(e)

    # Delete zipped datasets
    os.remove(zipped_dataset_path)


__all__ = ["install_datasets"]
