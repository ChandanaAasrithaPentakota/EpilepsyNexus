import numpy as np
import pickle
from pathlib import Path

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))
from graph import EpilepsyState
import joblib

MODEL_PATH = PROJECT_ROOT / "models" / "lightgbm.pkl"
eeg_model = joblib.load(MODEL_PATH)

import pandas as pd
import numpy as np
import joblib
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler


# =====================================================
# REBUILD SCALER
# =====================================================
df = pd.read_csv("/home/aasritha/EpilepsyNexus/trails/BEED_Data.csv")

X = df.drop("y", axis=1)

scaler = StandardScaler()
scaler.fit(X)


# =====================================================
# LABEL MAPPING
# =====================================================

def map_seizure_type(label: int) -> str:
    mapping = {
        0: "healthy",
        1: "generalized",
        2: "focal",
        3: "seizure with motor",
    }
    return mapping.get(label, "uncertain")


# =====================================================
# LOAD EEG
# =====================================================

def load_eeg_features(file_path: str):

    with open(file_path, "r") as f:
        text = f.read().strip()

    values = [float(x.strip()) for x in text.split(",") if x.strip()]

    features = np.array(values, dtype=np.float32).reshape(1, -1)

    # correct scaling
    features = scaler.transform(features)

    return features


# =====================================================
# EEG NODE
# =====================================================

def eeg_classifier_node(state: EpilepsyState) -> EpilepsyState:

    if state.eeg_text_file_path is None:
        state.seizure_type = "uncertain"
        return state

    try:
        features = load_eeg_features(state.eeg_text_file_path)

        pred = eeg_model.predict(features)[0]

        state.seizure_type = map_seizure_type(pred)

    except Exception as e:
        print("EEG error:", e)
        state.seizure_type = "uncertain"

    return state

if __name__ == "__main__":
    state = EpilepsyState(
        eeg_text_file_path="sample.txt"
    )

    result = eeg_classifier_node(state)
    print("Seizure type:", result.seizure_type)





