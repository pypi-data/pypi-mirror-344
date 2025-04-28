import gdown
from importlib import resources
import os
import rarfile

# Paths
datasets_dir = resources.files("myosotis_researches").joinpath("CcGAN", "datasets")

# File ID dictionary
file_id_dict = {
    "Ra": "1DJfpvXTX1x6Ldf4nZzqzlVsQSx9iXo9I",
    "MNIST": "1ZmTSX_wl68nsQI0ImfhpIsPClW_QrK1T",
}


# Function
def install_datasets(datasets_name):

    # Path
    zipped_dataset_path = os.path.join(datasets_dir, f"{datasets_name}_datasets.rar")

    # File ID
    file_id = file_id_dict[datasets_name]

    # URL
    url = f"https://drive.google.com/uc?id={file_id}"

    # Download
    gdown.download(url, zipped_dataset_path, quiet=False, use_cookies=False)

    # Unzip
    with rarfile.RarFile(zipped_dataset_path) as rf:
        if rf.needs_password():
            unzip_password = input("Password: ")
            rf.extractall(path=datasets_dir, pwd=unzip_password)
        else:
            rf.extractall(path=datasets_dir)

    # Delete zipped datasets
    os.remove(zipped_dataset_path)


__all__ = ["install_datasets"]
