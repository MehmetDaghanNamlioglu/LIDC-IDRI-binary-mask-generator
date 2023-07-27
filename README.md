# Code Overview
This script reads CT scan data from the LIDC-IDRI dataset and generates consensus masks for the nodules detected in the scans. The nodules are identified using the pylidc library. The generated masks are saved as PNG images. This is useful for tasks like image segmentation and the diagnosis of lung diseases.

## Dependencies
The script relies on the following Python packages:

os
pathlib
pylidc
configparser
PIL (Pillow)
numpy


Please note, the pylidc library requires a local installation of a DICOM-compatible database. More information can be found here.

## Usage

1. First, you need to specify the directories that contain your DICOM and mask data:

    - `DICOM_DIR`: This should be the directory containing your LIDC-IDRI DICOM files.
    - `MASK_DIR`: This is the directory where the masks will be stored. This directory will be created if it doesn't exist.

2. Additionally, you can set the confidence level (`confidence_level`) and padding size (`padding`) for pylidc's consensus function. 

3. Once your directories and hyperparameters are set, you can run the script:


Once your directories and hyperparameters are set, you can run the script

Script generate consensus masks for each nodule found in the scans. For each nodule, a PNG mask is created, either as a normal slice or a nodule-containing slice.
