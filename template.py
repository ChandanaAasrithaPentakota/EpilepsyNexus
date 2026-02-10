import os
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: %(message)s'
)

project_name = "EpilepsyNexus"

list_of_files = [

    "requirements.txt",
    "trials/",
    "llms/__init__.py",
    "llms/groq_llm.py",
    "prompts/mri_eeg_combiner_prompt.txt",
    "prompts/medical_rag_prompt.txt",
    "prompts/neuro_diagnostic_report_prompt.txt",
    "prompts/patient_communication_prompt.txt",
    "prompts/safe_guard_prompt.txt",
    "nodes/__init__.py",
    "nodes/mri_eeg_combiner.py",
    "nodes/medical_rag/",
    "nodes/neuro_diagnostic_report.py",
    "nodes/patient_communication.py",
    "nodes/safe_guard.py",
    "models/__init__.py",
    "models/load_mri_model.py",
    "models/load_eeg_model.py",
    "config.py",
    "graph.py",
    "template.py",
    "main.py",
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir:
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir}")

    if not filepath.exists():
        with open(filepath, "w") as f:
            pass
        logging.info(f"Created file: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")
