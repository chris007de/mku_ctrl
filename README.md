# MKU UP 2424 B Remote Script

This script enables to control the status of your Kuhne MKU UP 2424 B converter
using a handy webinterface.
Additionally, it provides a HTTP REST interface, which can be used for further
integration in your network (for API reference, see below).

# Running the script

## Run from source

After running the script, you can access the webinterface on `http://localhost:5000`

### Linux

1. Create virtual environment
    
    `python -m venv venv`

2. Activate virtual environment

    `source venv/bin/activate`

3. Install requirements

    `pip install -r requirements.txt`

4. Run script

    `python mku_ctrl.py /dev/ttyUSB0` (choose port accordingly)

### Windows

1. Install Miniconda from `https://docs.conda.io/en/latest/miniconda.html`

2. Create a new conda environment

    `conda create --name kuhne_mku_ctrl`

3. Switch to the new environment

    `conda activate kuhne_mku_ctrl`

4. Install requirements

    `python -m pip install requirements.txt`

5. Run script

    `python mku_ctrl.py COM1` (choose port accordingly)

### Building a standalone executable

1. Install Pyinstaller

    `python -m pip install PyInstaller`

2. Run

    `pyinstaller -w -F --add-data "templates;templates" --add-data "static;static" mku_ctrl.py`

3. Executable is generated to `./dist` folder, run it from commandline (e.g. `mku_ctrl.exe COM1`)

# REST API

Based on MKU UP 2424 B Manual v1.1 (21.10.2020)

## Read configuration

* /get/converter_state
* /get/pll_lock
* /get/converter_mode
* /get/forward_power
* /get/reverse_power
* /get/temperature
* /get/software_version

## Write Configuration

* /set/converter_state/[O0;O1]

The other write commands are not implemented (yet), as they are not needed
in everyday usage.
