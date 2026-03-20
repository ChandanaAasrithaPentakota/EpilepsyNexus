import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import cv2
import numpy as np
import tensorflow as tf

from tensorflow.keras.applications.efficientnet_v2 import preprocess_input
from graph import EpilepsyState


MODEL_PATH = PROJECT_ROOT / "models" / "efficientnet_v2_finetuned.h5"
model = tf.keras.models.load_model(MODEL_PATH)



def crop_brain(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # ✅ changed to RGB

    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) > 0:
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        image = image[y:y+h, x:x+w]

    return image


def preprocess_mri_inference(image):
    """
    MUST match training (EfficientNetV2 pipeline)
    """


    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


    image = crop_brain(image)


    image = cv2.resize(image, (224, 224))


    image = image.astype(np.float32)

    image = preprocess_input(image)

    return image


def mri_classifier_node(state: EpilepsyState) -> EpilepsyState:
    """
    MRI epilepsy classification
    """

    if state.mri_image_path is None:
        state.mri_epilepsy_label = "uncertain"
        return state

    try:

        img = cv2.imread(str(state.mri_image_path))

        if img is None:
            state.mri_epilepsy_label = "uncertain"
            return state


        processed = preprocess_mri_inference(img)


        processed = np.expand_dims(processed, axis=0)


        pred = model.predict(processed, verbose=0)[0][0]

      


        if pred > 0.5:
            label = "healthy"
        else:
            label = "epilepsy"

        state.mri_epilepsy_label = label

    except Exception as e:
        print("MRI error:", e)
        state.mri_epilepsy_label = "uncertain"

    return state