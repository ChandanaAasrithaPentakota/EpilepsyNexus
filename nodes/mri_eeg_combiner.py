import json
import sys
from pathlib import Path
from langchain_core.prompts import PromptTemplate
from graph import EpilepsyState
from llms.groq_llm import get_groq_llm

llm = get_groq_llm()
PROJECT_ROOT = Path.cwd().parent
sys.path.insert(0, str(PROJECT_ROOT))
print(PROJECT_ROOT)

prompt_path = PROJECT_ROOT / "EpilepsyNexus" / "prompts" / "mri_eeg_combiner_prompt.txt"
prompt = PromptTemplate(
    template=prompt_path.read_text(encoding="utf-8"),
    input_variables=[
        "mri_epilepsy_label",
        "seizure_phase",
        "seizure_type",
    ],
)


def mri_eeg_fusion_node(state: EpilepsyState) -> EpilepsyState:
    """
    Combines MRI and EEG classifier outputs using Groq LLM.
    Produces epilepsy_presence + fusion explanation.
    """

    # ---------- Read from state ----------
    inputs = {
        "mri_epilepsy_label": state.mri_epilepsy_label,
        # "mri_confidence": state.mri_confidence,
        "seizure_phase": state.seizure_phase,
        "seizure_type": state.seizure_type,
    }

    # ---------- Run LLM ----------
    response = llm.invoke(prompt.format(**inputs))

    # ---------- Parse JSON safely ----------
    try:
        output = json.loads(response.content)
    except json.JSONDecodeError:
        state.epilepsy_presence = "uncertain"
        state.fusion_explanation = (
            "Fusion agent could not reliably combine MRI and EEG findings."
        )
        return state

    # ---------- Write back to state ----------
    state.epilepsy_presence = output.get("epilepsy_presence")
    state.seizure_phase = output.get("seizure_phase")
    state.seizure_type = output.get("seizure_type")
    state.fusion_explanation = output.get("fusion_explanation")

    return state

formatted_prompt = prompt.format(
    mri_epilepsy_label="Temporal Lobe Epilepsy",
    seizure_phase="Ictal",
    seizure_type="Focal seizure"
)
####==========test=======#####
state = EpilepsyState(
    mri_epilepsy_label="epilepsy",
    mri_confidence=0.93,
    seizure_phase="ictal",
    seizure_type="focal",
)
state = mri_eeg_fusion_node(state)


print(json.dumps(state.model_dump(), indent=4))