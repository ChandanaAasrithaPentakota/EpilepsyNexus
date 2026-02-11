import json
import sys
from pathlib import Path
from langchain_core.prompts import PromptTemplate


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


from graph import EpilepsyState
from llms.groq_llm import get_groq_llm


PROJECT_ROOT = Path(__file__).resolve().parents[1]

prompt_path = PROJECT_ROOT / "prompts" / "neuro_diagnostic_report_prompt.txt"
with open(prompt_path, "r", encoding="utf-8") as f:
    template_text = f.read()



llm = get_groq_llm()


prompt = PromptTemplate(
    template=template_text,
    input_variables=[
        "epilepsy_presence",
        "seizure_phase",
        "seizure_type",
        "fusion_explanation",
        "medical_context",
    ],
    )


def neuro_diagnostic_report_node(state: EpilepsyState) -> EpilepsyState:
    """
    Generates a formal neurologist-style diagnostic report.
    """

    inputs = {
        "epilepsy_presence": state.epilepsy_presence,
        "seizure_phase": state.seizure_phase,
        "seizure_type": state.seizure_type,
        "fusion_explanation": state.fusion_explanation,
        "medical_context": state.medical_context,
    }


    response = llm.invoke(prompt.format(**inputs))


    state.neuro_diagnostic_report = response.content

    return state

