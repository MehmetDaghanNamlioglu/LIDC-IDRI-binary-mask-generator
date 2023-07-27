import os
from pathlib import Path
import pylidc as pl
from configparser import ConfigParser
from pylidc.utils import consensus
from PIL import Image
import numpy as np



# Get Directory setting
DICOM_DIR = "/opt/jupyterlab/Datasets/CT/Lungs/LIDC-IDRI/manifest-1600709154662/LIDC-IDRI" #parser.get('prepare_dataset','LIDC_DICOM_PATH')
MASK_DIR = "./masks_final_0consensus/Mask" 

# Hyper Parameter setting for pylidc
confidence_level = 0.01 
padding = 512

# Ensure the mask directory exists
if not os.path.exists(MASK_DIR):
    os.makedirs(MASK_DIR)

# Get the list of all patients
LIDC_IDRI_list= [f for f in os.listdir(DICOM_DIR) if not f.startswith('.')]
LIDC_IDRI_list.sort()
#LIDC_IDRI_list =  ['LIDC-IDRI-0049']

for patient in LIDC_IDRI_list:
    pid = patient 
    scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == pid).first()
    nodules_annotation = scan.cluster_annotations()
    vol = scan.to_volume()

    patient_mask_dir = Path(MASK_DIR) / pid
    Path(patient_mask_dir).mkdir(parents=True, exist_ok=True)

    # Generate consensus masks for each nodule
    consensus_masks = []
    for nodule_idx, nodule in enumerate(nodules_annotation):
        mask, cbbox, masks = consensus(nodule, confidence_level, [(padding, padding), (padding, padding), (0, 0)])
        consensus_masks.append((mask, cbbox))
    total_slices = vol.shape[-1]

    for slice_index in range(vol.shape[-1]):
        mask_slice = np.zeros_like(vol[:,:,slice_index], dtype=np.uint8)
        nodule_in_slice = False
        reverse_slice_index = total_slices - slice_index

        for mask, cbbox in consensus_masks:
            if cbbox[2].start <= slice_index < cbbox[2].stop:
                # If the current slice is within the bounding box of the nodule
                mask_slice |= mask[:,:,slice_index - cbbox[2].start]
                nodule_in_slice = True

        if nodule_in_slice:
            mask_name = "{}_mask_slice{}N".format(pid[-4:], str(reverse_slice_index).zfill(3))
        else:
            mask_name = "{}_mask_slice{}".format(pid[-4:], str(reverse_slice_index).zfill(3))
        
        # Save the mask
        Image.fromarray(mask_slice).save(patient_mask_dir / (mask_name + '.png'))
