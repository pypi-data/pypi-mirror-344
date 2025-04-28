# Myosotis-Researches

## `CcGAN` (`myosotis_researches.CcGAN`)

### `internal`

The `internal` module is used for setting the local package itself, like installing datasets and so on.

Import with code

```python
from myosotis_researches.internal import *
```

| Function                          | Desctiption                                                  |
| --------------------------------- | ------------------------------------------------------------ |
| `install_datasets(datasets_name)` | Install the datasets in `datasets_name` to the local python package. |
| `uninstall_datasets()`            | Remove all the datasets installed to the local python package. |
| `show_datasets()`                 | Show all datasets installed.                                 |

**Note**:

1. The path of the installed datasets are

   `resources.files("myosotis_researches").join("CcGAN", "<datasets_name>")`

   To run this code, remember to add `from importlib import resources` at the beginning.

### `utils`

The `utils` module contains some basic functions and classes which are frequently used during the CcGAN research.

Import with code

```python
from myosotis_researches.utils import *
```

| Function                                              | Description                               |
| ----------------------------------------------------- | ----------------------------------------- |
| `concat_image(img_list, gap=2, direction="vertical")` | Concat images vertically or horizontally. |
| `print_hdf5(name, obj)`                               | Print a basic structure of an HDF5 file.  |

**Note**:

1. Function `print_hdf5` should be used within a `with` block:

   ```python
   import h5py
   
   with h5py.File(<HDF5_file_path>, "r") as f:
     f.visititems(print_hdf5)
   ```
