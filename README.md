# Face detection webservice

<html>
<p align="center">
    <img src="docs/assets/logo.png" alt="Logo" width="100">
</p>
</html>

## Installation
```bash
# Clone the repo **with submodules**
git clone --recurse-submodules 
cd 
# if you already cloned without --recurse-submodules:
git submodule update --init --recursive

# Create standalone miniforge (an Anaconda alternative) environment, but any other Python environment should also work
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh -b -p $PWD/env
source env/bin/activate

# Install python 3.10.12
conda install python=3.10.12

# Install motionalbums package in editable mode and its requirements
# Editable mode is currently required to locate packages from the submodules
python -m pip install -e .
```

## Project Structure

```lua
/facedetectionapp
|-- src/
  |-- facedetectionapp/
    |-- insightface_wrapper.py
    |-- main.py
    |-- sandbox.py
|-- tests/
  |-- unit/
    |-- facedetectionapp/
      |-- test_main.py
|-- Dockerfile
|-- CODE_CONVENTION.md
|-- README.md
|-- requirements.txt
```
