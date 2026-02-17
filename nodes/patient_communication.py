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

prompt_path = PROJECT_ROOT / "EpilepsyNexus" / "prompts" / "patient_communication_prompt.txt"
prompt = PromptTemplate(
    template=prompt_path.read_text(encoding="utf-8"),
    input_variables=[
    "neuro_diagnostic_report",
    ],
)

def patient_communication_node(state: EpilepsyState) -> EpilepsyState:
    if not state.neuro_diagnostic_report:
        state.patient_explanation = (
            "No diagnostic report available. Please consult a neurologist."
        )
        return state
    inputs = {
        "neuro_diagnostic_report": state.neuro_diagnostic_report,
    }
    response = llm.invoke(prompt.format(**inputs))
    try:
        output = json.loads(response.content)
    except json.JSONDecodeError:
        state.patient_explanation = (
            "A simplified explanation could not be generated at this time. "
            "Please consult a neurologist for detailed interpretation."
        )
        return state
    state.patient_explanation = output.get("patient_explanation")

    return state

 