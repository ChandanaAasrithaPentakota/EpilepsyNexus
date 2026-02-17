import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


import cv2
import numpy as np
import tensorflow as tf
from pathlib import Path


from graph import EpilepsyState

MODEL_PATH = PROJECT_ROOT / "models" / "efficientnet_v2_finetuned.h5"
model = tf.keras.models.load_model(MODEL_PATH)

def crop_brain(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) > 0:
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        image = image[y:y+h, x:x+w]

    return image




def resize_image(image, size=224):
    return cv2.resize(image, (size, size))


def preprocess_mri_inference(image):
    """
    EXACT match with your saved training dataset.
    """

    # ---- crop ----
    image = crop_brain(image)

    # ---- resize ----
    image = resize_image(image)

    # ---- same min-max scaling ----
    image = image.astype(np.float32)
    image = (image - image.min()) / (image.max() - image.min() + 1e-8)

    # ---- convert to uint8 (same as saved dataset) ----
    image = (image * 255).astype(np.uint8)

    # ---- final normalization ----
    image = image.astype(np.float32) / 255.0

    return image


# =====================================================
# 3️⃣ MRI NODE
# =====================================================

def mri_classifier_node(state: EpilepsyState) -> EpilepsyState:
    """
    MRI epilepsy classification.
    """

    if state.mri_image_path is None:
        state.mri_epilepsy_label = "uncertain"
        return state

    try:
        # ---- load image ----
        img = cv2.imread(state.mri_image_path)

        if img is None:
            state.mri_epilepsy_label = "uncertain"
            return state

        # ---- preprocess ----
        processed = preprocess_mri_inference(img)

        # ---- add batch ----
        processed = np.expand_dims(processed, axis=0)


        # ---- predict ----
        pred = model.predict(processed, verbose=0)[0][0]



        # ---- your threshold rule ----
        if pred <= 0.5:
            label = "epilepsy"
        else:
            label = "healthy"

        state.mri_epilepsy_label = label

    except Exception as e:
        print("MRI error:", e)
        state.mri_epilepsy_label = "uncertain"

    return state


