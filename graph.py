from pydantic import BaseModel, Field
from typing import Optional, List

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
