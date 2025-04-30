import h5py
from importlib import resources
import os

datasets_dir = resources.files("myosotis_researches").joinpath("CcGAN", "datasets")


def make_h5(
    old_datasets_name,
    size,
    new_datasets_path,
    image_indexes,
    train_indexes,
    val_indexes,
):

    old_datasets_path = os.path.join(
        datasets_dir, f"{old_datasets_name}_datasets", f"{old_datasets_name}_{size}x{size}.h5"
    )

    with h5py.File(old_datasets_path, "r") as f:
        image_datas = f["images"][:]
        image_labels = f["labels"][:]
        image_types = f["types"][:]

    with h5py.File(new_datasets_path, "w") as f:
        f.create_dataset("images", data=image_datas[image_indexes])
        f.create_dataset("indx_train", data=train_indexes)
        f.create_dataset("indx_valid", data=val_indexes)
        f.create_dataset("labels", data=image_labels[image_indexes])
        f.create_dataset("types", data=image_types[image_indexes])


__all__ = ["make_h5"]
