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


# download_dataset
_file_id_dict = {
    "Ra": "1YVLFAaQ1ldre0ASLSRdV_kPIcAMkwGqO",
    "MNIST": "18249ryrDPsznWWtOkJuALZWCVoZqfibC",
}


def download_dataset(dataset_name, dataset_path):
    dataset_dir = os.path.dirname(dataset_path)
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir, exist_ok=True)
    zipped_dataset_path = os.path.join(dataset_dir, f"{dataset_name}.rar")
    file_id = _file_id_dict[dataset_name]
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, zipped_dataset_path, quiet=False, use_cookies=False)
    unzip_password = getpass.getpass("Please input the zipped file's password:")
    try:
        cmd = ["unrar", "x", f"-p{unzip_password}", zipped_dataset_path, dataset_dir]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(e)
    os.remove(zipped_dataset_path)


__all__ = ["view_dataset", "download_dataset"]
