import json
import sys
from pathlib import Path
from langchain_core.prompts import PromptTemplate
from graph import EpilepsyState
from llms.groq_llm import get_groq_llm
import re

llm = get_groq_llm()
PROJECT_ROOT = Path.cwd().parent
sys.path.insert(0, str(PROJECT_ROOT))

prompt_path = PROJECT_ROOT / "EpilepsyNexus" / "prompts" / "safe_guard_prompt.txt"
prompt = PromptTemplate(
    template=prompt_path.read_text(encoding="utf-8"),
    input_variables=[
    "neuro_diagnostic_report",
    "patient_explanation",
    ],
)

def safe_guard_node(state: EpilepsyState) -> EpilepsyState:
    if not state.neuro_diagnostic_report or not state.patient_explanation:
        state.safety_passed = False
        state.safety_notes = "Missing report or patient explanation."
        return state

    inputs = {
        "neuro_diagnostic_report": state.neuro_diagnostic_report,
        "patient_explanation": state.patient_explanation,
    }

    try:
        response = llm.invoke(prompt.format(**inputs))
        content = response.content.strip()
        content = re.sub(r"```json|```", "", content).strip()
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            content = match.group(0)
        output = json.loads(content)


        state.safety_passed = output.get("safety_passed", False)
        state.safety_notes = output.get("safety_notes", "No safety notes provided.")

    except json.JSONDecodeError:
        state.safety_passed = False
        state.safety_notes = "Safety Guard failed to return valid JSON."

    except Exception as e:
        state.safety_passed = False
        state.safety_notes = f"Unexpected error in Safety Guard: {str(e)}"

    return state

 