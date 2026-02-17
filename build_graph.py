
import numpy as np
import pickle
from pathlib import Path


import sys
from pathlib import Path

from langgraph.graph import StateGraph, END
from graph import EpilepsyState


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from nodes.mri_classifier import mri_classifier_node
from nodes.eeg_classifier import eeg_classifier_node
from nodes.mri_eeg_combiner import mri_eeg_fusion_node
from nodes.medical_rag import medical_rag_node
from nodes.neuro_diagnostic_report import neuro_diagnostic_report_node
from nodes.patient_communication import patient_communication_node
from nodes.safe_guard import safe_guard_node



def build_graph():

    workflow = StateGraph(EpilepsyState)

    # ---- Add nodes ----
    workflow.add_node("mri_classifier", mri_classifier_node)
    workflow.add_node("eeg_classifier", eeg_classifier_node)
    workflow.add_node("fusion", mri_eeg_fusion_node)
    workflow.add_node("medical_rag", medical_rag_node)
    workflow.add_node("neuro_report", neuro_diagnostic_report_node)
    workflow.add_node("patient", patient_communication_node)
    workflow.add_node("safety", safe_guard_node)

    # ---- Flow ----
    workflow.set_entry_point("mri_classifier")

    workflow.add_edge("mri_classifier", "eeg_classifier")
    workflow.add_edge("eeg_classifier", "fusion")
    workflow.add_edge("fusion", "medical_rag")
    workflow.add_edge("medical_rag", "neuro_report")
    workflow.add_edge("neuro_report", "patient")
    workflow.add_edge("patient", "safety")

    workflow.add_edge("safety", END)

    return workflow.compile()


