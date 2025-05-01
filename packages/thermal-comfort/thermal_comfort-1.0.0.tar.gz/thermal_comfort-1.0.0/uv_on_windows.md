# Package manager `UV`

[uv](https://docs.astral.sh/uv/) is an extremely fast Python package and project
manager, written in Rust.

It makes working with python environments much, much faster.

## Installation

### MacOS

1. use this command to install `uv`

   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

1. now check if the installation was successful (should return the version instantly)

   ```powershell
   uv --version
   ```

   it should show you something like this:

   ```console
   uv 0.5.16 (333f03f11 2025-01-08)
   ```

1. now create a new environment

   - `geo-python` is the name of the environment. You can choose any name, commonly it's
     also called `venv` which stands for virtual environment.
   - `--python 3.12` choses the python version to use. This can be any (recent) version
     available

   ```powershell
   uv venv geo-python --python 3.12
   ```

   This will download, if needed, python and create a virtual environment using that
   version. This will take approximately 1 -2 seconds and show this output:

   ```console
   Using CPython 3.13.1
   Creating virtual environment at: geo-python
   Activate with: geo-python/bin/activate
   ```

1. finally, we need to activate the environment with the suggested comment

   ```powershell
   geo-python/bin/activate
   ```

   This should work instantly and prepend `geo-python` to your terminal

   ```console
   (geo-python) $
   ```

1. Now continue with 6. from the windows guide

### Windows

The
[installation on windows](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)
works like this:

1. In vscode open a new Powershell terminal and paste this code. (download and
   installation takes 10 - 20 seconds)

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

1. Now paste this into the terminal (should succeed instantly with no output)

   ```
   $env:Path = "C:\Users\kittnjdr\.local\bin;$env:Path"
   ```

1. now check if the installation was successful (should return the version instantly)

   ```powershell
   uv --version
   ```

   it should show you something like this:

   ```console
   uv 0.5.16 (333f03f11 2025-01-08)
   ```

1. now create a new environment

   - `geo-python` is the name of the environment. You can choose any name, commonly it's
     also called `venv` which stands for virtual environment.
   - `--python 3.12` choses the python version to use. This can be any (recent) version
     available

   ```powershell
   uv venv geo-python --python 3.12
   ```

   This will download, if needed, python and create a virtual environment using that
   version. This will take approximately 1 -2 seconds and show this output:

   ```console
   Using CPython 3.13.1
   Creating virtual environment at: geo-python
   Activate with: geo-python\Scripts\activate
   ```

1. finally, we need to activate the environment with the suggested comment

   ```powershell
   geo-python\Scripts\activate
   ```

   This should work instantly and prepend `geo-python` to your terminal

   ```console
   (geo-python) PS C:\Users\kittnjdr\Documents\geo-python>
   ```

1. install the needed requirements

   Create a new file called `requirements.txt` in the root of your workspace. Add all
   packages you want to install e.g. these file contents

   ```
   cartopy
   contextily
   folium
   geopandas
   geopy
   mapclassify
   matplotlib
   numpy
   pandas
   pytest
   pytest-cov
   rasterio
   scikit-learn
   scipy
   seaborn
   shapely
   ```

   Now install the required packages

   ```powershell
   uv pip install -r requirements.txt
   ```

   For all the above packages this should take 10 seconds.

1. finally try if all worked by creating a file e.g. `test_my_imports.py` with these
   contents:

   ```python
   import cartopy
   import contextily
   import geopandas
   import geopy
   import matplotlib
   import numpy
   import pandas
   import pytest
   import rasterio
   import sklearn
   import scipy
   import seaborn
   import shapely
   ```

   And run it by using the "play" button. If you need to select your python in vscode
   (bottom right) select the version in your current working directory (starting with
   `.\<name of your virtual environment>`)

   ![](https://github.com/user-attachments/assets/2c0ca2f9-fb8f-4fcf-9b14-7b4a9e4c6e5d)

   There should be no error!

## FAQ

### What happened?

`uv` is, similar to conda, a package manager, however it's fast. In 1. we installed `uv`
itself, which saved it our User's directory, so we don't need admin privileges to
install it. In 2. we added it to our `PATH` which allows us to type `uv` in the terminal
and the shell knows what `uv` is. In 4. we create a virtual environment, similar to a
conda environment. The virtual environment ist just a folder in your working directory
containing all packages - no magic involved. In 5. we activate the environment, telling
our shell what environment to use. In 6. we install all packages. `-r` tells the
installer to use the `requirements.txt` file and install everything in there. In 7. we
simply check that all imports work as expected.

### How can I remove the environment

The virtual environment ist **only** the one folder created e.g. `geo-python`. Just
delete that folder, and the environment is gone.

### How can I add an additional package to my environment?

You can install a specific package like this:

```powershell
uv pip install solpos

```

```console
Using Python 3.13.1 environment at: geo-python
Resolved 1 package in 289ms
Prepared 1 package in 121ms
Installed 1 package in 31ms
 + solpos==0.1.2
```

This should only take a few milliseconds to seconds for most packages

### How can I remove a package from my environment?

You can uninstall a specific package like this:

```
uv pip uninstall solpos
```

```console
Using Python 3.13.1 environment at: geo-python
Uninstalled 1 package in 12ms
 - solpos==0.1.2
```

### Can I create a 2nd environment

Yes, you just have to chose a different name:

```powershell
uv venv python-course --python 3.12
```

and activate the environment you want

```
python-course\Scripts\activate

```

### How can I see what environment is active?

The active environment is prepended to your shell input

```console
(python-course) PS C:\Users\kittnjdr\Documents\geo-python>
```

or

```console
(geo-python) PS C:\Users\kittnjdr\Documents\geo-python>
```

Additionally, you may change it for vscode on the bottom-right.

### I cannot run my notebooks

When I click install in the dialog, vscode fails to install it

You will need to install the `iypkernel` package via `uv`

```console
uv pip install ipykernel
```

### How can I uninstall `uv`?

```powershell
# Remove all data that uv has stored
uv cache clean
rm -r "$(uv python dir)"
rm -r "$(uv tool dir)"
# Remove binaries
rm ~/.local/bin/uv ~/.local/bin/uvx
```
