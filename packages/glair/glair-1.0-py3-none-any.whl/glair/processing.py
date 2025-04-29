import os
import numpy as np
import nibabel as nib
import tensorflow as tf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import binary_fill_holes
from matplotlib.animation import FuncAnimation, PillowWriter
from tensorflow.keras import layers, Model
def load_from_directory(patient_dir, MODALITIES: int = 1, IMG_SIZE: tuple = (256, 256) ):
   
    slices = []
    weeks = sorted(
        d for d in os.listdir(patient_dir)
        if os.path.isdir(os.path.join(patient_dir, d)) and d.startswith("week-")
    )
    for w in weeks:
        week_dir = os.path.join(patient_dir, w)
        chan_slices = []
        for mod in MODALITIES:
            matches = [f for f in os.listdir(week_dir)
                       if mod.upper() in f.upper() and f.endswith('.nii.gz')]
            source = week_dir
            if not matches:
                fallback = os.path.join(week_dir, "HD-GLIO-AUTO-segmentation", "native")
                if os.path.isdir(fallback):
                    source = fallback
                    matches = [f for f in os.listdir(fallback)
                               if mod.upper() in f.upper() and f.endswith('.nii.gz')]
            if matches:
                path = os.path.join(source, matches[0])
                try:
                    vol = nib.load(path).get_fdata()
                    mid = vol.shape[2] // 2
                    slice2d = vol[..., mid]
                    if mod == 'CT1':
                        slice2d = (slice2d > 0).astype(np.float32)
                    else:
                        mn, mx = slice2d.min(), slice2d.max()
                        slice2d = ((slice2d - mn) / (mx - mn + 1e-8)).astype(np.float32)
                except Exception:
                    slice2d = np.zeros(IMG_SIZE, dtype=np.float32)
            else:
                slice2d = np.zeros(IMG_SIZE, dtype=np.float32)
            resized = tf.image.resize(slice2d[..., None], IMG_SIZE).numpy()
            chan_slices.append(resized)
        img = np.concatenate(chan_slices, axis=-1)
        slices.append(img)
    return slices
