import gdown
import getpass
import h5py
import os
import subprocess


# view_dataset
def _print_hdf5(name, obj):
    indent = "  " * name.count("/")
    if isinstance(obj, h5py.Dataset):
        print(f"{indent}[Dataset] {name} shape={obj.shape} dtype={obj.dtype}")
    elif isinstance(obj, h5py.Group):
        print(f"{indent}[Group]   {name}")


def view_dataset(dataset_path):
    with h5py.File(dataset_path, "r") as f:
        f.visititems(_print_hdf5)


# download_datasets
_file_id_dict = {
    "Ra": "1YVLFAaQ1ldre0ASLSRdV_kPIcAMkwGqO",
    "MNIST": "18249ryrDPsznWWtOkJuALZWCVoZqfibC",
}


def download_datasets(datasets_name, datasets_dir):
    if not os.path.exists(datasets_dir):
        os.makedirs(datasets_dir, exist_ok=True)
    zipped_datasets_path = os.path.join(datasets_dir, f"{datasets_name}.rar")
    file_id = _file_id_dict[datasets_name]
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, zipped_datasets_path, quiet=False, use_cookies=False)
    unzip_password = getpass.getpass("Please input the zipped file's password:")
    try:
        cmd = ["unrar", "x", f"-p{unzip_password}", zipped_datasets_path, datasets_dir]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(e)
    os.remove(zipped_datasets_path)


__all__ = ["view_dataset", "download_datasets"]
