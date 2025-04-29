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

# ─── CONFIG ────────────────────────────────────────────────────────────────────
#DATA_DIR      = "/home/josh/Desktop/data"
#MODALITIES    = ['CT1', 'T1', 'T2', 'FLAIR']
#IMG_SIZE      = (128, 128)
#SEQ_IN        = 2    # number of past frames to use as input
#SEQ_OUT       = 1  # number of future frames to predict
#INTERP_STEPS  = 8
MODEL_PATH    = "vae_convlstm_model_multimodal_with_gamma.keras"
#NUM_PATIENTS  = 3

# ─── VAE CONVLSTM MODEL DEFINITION (unchanged) ─────────────────────────────────
class VAE_ConvLSTM(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.encoder = tf.keras.Sequential([
            layers.ConvLSTM2D(64, (3, 3), padding='same', return_sequences=True, activation='relu'),
            layers.ConvLSTM2D(32, (3, 3), padding='same', return_sequences=False, activation='relu'),
            layers.Flatten(),
        ])
        self.z_mean = layers.Dense(128, name='z_mean')
        self.z_log_var = layers.Dense(128, name='z_log_var')
        self.decoder_fc = layers.Dense(32 * 32 * 32, activation='relu')
        self.decoder_reshape = layers.Reshape((32, 32, 32))
        self.decoder_up1 = layers.Conv2DTranspose(64, (3, 3), strides=2, padding='same', activation='relu')
        self.decoder_up2 = layers.Conv2DTranspose(32, (3, 3), strides=2, padding='same', activation='relu')
        self.decoder_out = layers.Conv2D(1, (3, 3), padding='same', activation='sigmoid')

    def sample(self, z_mean, z_log_var):
        epsilon = tf.random.normal(shape=tf.shape(z_mean))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

    def call(self, inputs):
        x = self.encoder(inputs)
        z_mean = self.z_mean(x)
        z_log_var = self.z_log_var(x)
        z = self.sample(z_mean, z_log_var)
        kl_loss = -0.5 * tf.reduce_mean(1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
        self.add_loss(kl_loss)
        x = self.decoder_fc(z)
        x = self.decoder_reshape(x)
        x = self.decoder_up1(x)
        x = self.decoder_up2(x)
        return self.decoder_out(x)

# ─── LOAD MULTI-MODAL SLICES (unchanged) ────────────────────────────────────────
def load_patient_slices(patient_dir, MODALITIES, IMG_SIZE):
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

# ─── FRAME INTERPOLATION & METRIC (unchanged) ─────────────────────────────────
def interpolate_frames(frames, n_steps):
    out = []
    for a, b in zip(frames, frames[1:]):
        for alpha in np.linspace(0, 1, n_steps, endpoint=False):
            out.append((1-alpha)*a + alpha*b)
    out.append(frames[-1])
    return out

def dice_coefficient(y_true, y_pred, smooth=1e-6):
    inter = np.sum(y_true * y_pred)
    return (2.*inter + smooth) / (np.sum(y_true) + np.sum(y_pred) + smooth)

# ─── MAIN EVALUATION ──────────────────────────────────────────────────────────
def vae_predict(DATA_DIR, SEQ_IN, SEQ_OUT, NUM_PATIENTS, INTERP_STEPS):
    # 1. Select patients with at least SEQ_IN timepoints
    patients = sorted(d for d in os.listdir(DATA_DIR) if d.startswith("Patient-"))
    selected = []
    for p in patients:
        slices = load_patient_slices(os.path.join(DATA_DIR, p))
        if len(slices) >= SEQ_IN:
            selected.append((p, slices))
        if len(selected) == NUM_PATIENTS:
            break
    if len(selected) < NUM_PATIENTS:
        raise RuntimeError(f"Only found {len(selected)} patients with at least {SEQ_IN} timepoints.")

    # 2. Load trained multimodal VAE
    model = tf.keras.models.load_model(
        MODEL_PATH,
        custom_objects={'VAE_ConvLSTM': VAE_ConvLSTM},
        compile=False
    )

    # 3. Iterate patients and predict SEQ_OUT horizons
    for pname, slices in selected:
        # Extract CT1 channel for simplicity
        ct_slices = [s[...,0] for s in slices]
        preds = []
        truths = []
        for i in range(SEQ_OUT):
            start = i
            end = i + SEQ_IN
            if end > len(ct_slices):
                break
            # prepare input batch
            inp_seq = np.stack([slices[j] for j in range(start, end)], axis=0)
            inp = inp_seq[None, ...]
            # predict next frame
            pred_full = model.predict(inp)[0]
            pred_mask = pred_full[...,0]
            preds.append(pred_mask)
            # select truth or freeze last
            truth_idx = end
            if truth_idx < len(ct_slices):
                truths.append(ct_slices[truth_idx])
            else:
                truths.append(ct_slices[-1])

        # 4. Compute metrics per-horizon
        for h, (pred_frame, truth_frame) in enumerate(zip(preds, truths), 1):
            mse = np.mean((truth_frame - pred_frame)**2)
            ssim = tf.image.ssim(
                truth_frame[...,None], pred_frame[...,None], max_val=1.0
            ).numpy().mean()
            dice = dice_coefficient(truth_frame>0.5, pred_frame>0.5)
            print(f"Patient: {pname} | Horizon {h} | MSE: {mse:.4f}, SSIM: {ssim:.4f}, Dice: {dice:.4f}")

        # 5. Build animation sequence
        pairs = []
        # first, inputs
        input_seq = ct_slices[:SEQ_IN]
        for a, b in zip(input_seq[:-1], input_seq[1:]):
            for f in interpolate_frames([a, b], INTERP_STEPS):
                pairs.append((f, f, 'Input','Input'))
        # then, predictions
        prev = input_seq[-1]
        for (pred_f, truth_f) in zip(preds, truths):
            pred_seg = interpolate_frames([prev, pred_f], INTERP_STEPS)
            truth_seg = interpolate_frames([prev, truth_f], INTERP_STEPS)
            for pframe, tframe in zip(pred_seg, truth_seg):
                pairs.append((pframe, tframe, 'Prediction','Ground Truth'))
            prev = pred_f

        # 6. Plot & save GIF
        fig, (ax1, ax2) = plt.subplots(1,2,figsize=(8,4))
        im1 = ax1.imshow(pairs[0][0], cmap='gray', vmin=0, vmax=1)
        m1  = ax1.imshow(binary_fill_holes(pairs[0][0]>0.5), cmap='gray', vmin=0, vmax=1, alpha=0.5)
        ax1.axis('off'); ax1.set_title(pairs[0][2])
        im2 = ax2.imshow(pairs[0][1], cmap='gray', vmin=0, vmax=1)
        m2  = ax2.imshow(binary_fill_holes(pairs[0][1]>0.5), cmap='gray', vmin=0, vmax=1, alpha=0.5)
        ax2.axis('off'); ax2.set_title(pairs[0][3])

        def update(frame):
            pimg, timg, t1, t2 = pairs[frame]
            im1.set_data(pimg); m1.set_data(binary_fill_holes(pimg>0.5)); ax1.set_title(t1)
            im2.set_data(timg); m2.set_data(binary_fill_holes(timg>0.5)); ax2.set_title(t2)
            return im1, m1, im2, m2

        anim = FuncAnimation(fig, update, frames=len(pairs), interval=200, blit=True)
        out_gif = f"eval_{pname}.gif"
        anim.save(out_gif, writer=PillowWriter(fps=5))






        


        
        print(f"Saved animated GIF: {out_gif}")
