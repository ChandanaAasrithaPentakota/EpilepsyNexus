import json
import sys
from pathlib import Path
from langchain_core.prompts import PromptTemplate
from graph import EpilepsyState
from llms.groq_llm import get_groq_llm

llm = get_groq_llm()
PROJECT_ROOT = Path.cwd().parent
sys.path.insert(0, str(PROJECT_ROOT))

prompt_path = PROJECT_ROOT / "EpilepsyNexus" / "prompts" / "mri_eeg_combiner_prompt.txt"

prompt = PromptTemplate(
    template=prompt_path.read_text(encoding="utf-8"),
    input_variables=[
        "mri_epilepsy_label",
        "seizure_type",
        "symptoms_text",
    ],
)


def mri_eeg_fusion_node(state: EpilepsyState) -> EpilepsyState:
    """
    Combines MRI result + EEG seizure type + patient symptoms.
    Produces:
    - epilepsy_presence
    - seizure_type
    - seizure_phase
    - fusion_explanation
    """
    inputs = {
        "mri_epilepsy_label": state.mri_epilepsy_label,
        "seizure_type": state.seizure_type,
        "symptoms_text": state.symptoms_text,
    }
    response = llm.invoke(prompt.format(**inputs))
    try:
        output = json.loads(response.content)
    except json.JSONDecodeError:
        state.epilepsy_presence = "uncertain"
        state.seizure_phase = "uncertain"
        state.seizure_type = "not_applicable"
        state.fusion_explanation = (
            "Fusion agent could not reliably combine MRI, EEG, and symptoms."
        )
        return state
    state.epilepsy_presence = output.get("epilepsy_presence")
    state.seizure_phase = output.get("seizure_phase")
    state.seizure_type = output.get("seizure_type")
    state.fusion_explanation = output.get("fusion_explanation")

    return state
