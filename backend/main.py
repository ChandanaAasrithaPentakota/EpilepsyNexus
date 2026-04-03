import sys
import shutil
import tempfile
from pathlib import Path

# Make sure the project root is on the path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from build_graph import build_graph
from graph import EpilepsyState

app = FastAPI(title="EpilepsyNexus API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()


@app.post("/analyze")
async def analyze(
    mri: UploadFile = File(..., description="MRI image file"),
    eeg: UploadFile = File(..., description="EEG .txt file"),
    symptoms: str = Form(..., description="Patient symptom description"),
):
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        mri_path = tmp_dir / mri.filename
        eeg_path = tmp_dir / eeg.filename

        with open(mri_path, "wb") as f:
            shutil.copyfileobj(mri.file, f)
        with open(eeg_path, "wb") as f:
            shutil.copyfileobj(eeg.file, f)

        state = EpilepsyState(
            mri_image_path=str(mri_path),
            eeg_text_file_path=str(eeg_path),
            symptoms_text=symptoms,
        )

        result = graph.invoke(state)

        # LangGraph returns a dict; convert to plain dict if needed
        if hasattr(result, "model_dump"):
            output = result.model_dump()
        elif isinstance(result, dict):
            output = result
        else:
            output = dict(result)

        # Strip file paths from response (not useful to client)
        output.pop("mri_image_path", None)
        output.pop("eeg_text_file_path", None)

        return output

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
