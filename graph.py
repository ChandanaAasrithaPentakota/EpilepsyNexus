from pydantic import BaseModel, Field
from typing import Optional, List
import numpy as np
import pickle
from pathlib import Path

import sys
from pathlib import Path

class EpilepsyState(BaseModel):
    # ========= RAW INPUTS =========
    mri_image_path: Optional[str] = Field(
        default=None,
        description="Path to input MRI image"
    )

    eeg_text_file_path: Optional[str] = Field(
        default=None,
        description="Path to EEG text file containing 50 comma-separated segments"
    )
    symptoms_text: Optional[str] = None  


    # ========= MRI CLASSIFIER OUTPUT =========
    mri_epilepsy_label: Optional[str] = Field(
        default=None,
        description="MRI classification: epilepsy or healthy"
    )


    # ========= EEG CLASSIFIER OUTPUT =========
    seizure_phase: Optional[str] = Field(
        default=None,
        description="EEG seizure phase (interictal, preictal, ictal, postictal)"
    )

    seizure_type: Optional[str] = Field(
        default=None,
        description="EEG seizure type (focal, generalized, unknown)"
    )

    # ========= MRI + EEG FUSION AGENT OUTPUT =========
    epilepsy_presence: Optional[str] = Field(
        default=None,
        description="Final epilepsy presence after fusion: yes / no / uncertain"
    )

    fusion_explanation: Optional[str] = Field(
        default=None,
        description="Explanation combining MRI and EEG findings"
    )

    # ========= MEDICAL RAG AGENT OUTPUT =========
    medical_context: Optional[str] = Field(
        default=None,
        description="Retrieved medical knowledge (guidelines, future steps, care)"
    )

    # ========= NEURO-DIAGNOSTIC REPORT AGENT OUTPUT =========
    neuro_diagnostic_report: Optional[str] = Field(
        default=None,
        description="Formal neurologist-style diagnostic report"
    )

    # ========= PATIENT COMMUNICATION AGENT OUTPUT =========
    patient_explanation: Optional[str] = Field(
        default=None,
        description="Simplified patient-friendly explanation"
    )

    # ========= SAFETY GUARD =========
    safety_passed: bool = Field(
        default=False,
        description="Whether output passed safety checks"
    )

    safety_notes: Optional[str] = Field(
        default=None,
        description="Notes or corrections added by safety guard"
    )


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))
from nodes.mri_classifier import mri_classifier_node
from nodes.eeg_classifier import eeg_classifier_node
from nodes.mri_eeg_combiner import fusion_node
from nodes.medical_rag import medical_rag_node
from nodes.neuro_diagnostic_report import neuro_diagnostic_report_node
from nodes.patient_communication import patient_communication_node
from nodes.safe_guard import safety_guard_node
