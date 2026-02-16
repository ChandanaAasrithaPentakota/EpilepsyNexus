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

                                    ####=====test==========####

state = EpilepsyState(
    neuro_diagnostic_report="""
    
                    Seizure Phase:
                    Ictal

                    Seizure Type:
                    Focal

                    Epilepsy Presence (Fusion Result):
                    Yes

                    Fusion Explanation:
                    Both MRI and EEG findings suggest focal seizure activity.

                    Retrieved Medical Context:
                    Focal""",
    patient_explanation="""
                 The recent brain scan and electrical testing that were done together show patterns 
                 that could indicate a type of seizure that starts in a specific area of the brain. 
                 This pattern is often called a focal seizure, meaning the activity begins in one region
                 rather than spreading across the whole brain at once. Because the findings from both the 
                 imaging and the electrical study point in the same direction, the results may suggest the 
                 presence of an ongoing seizure condition. It is important to remember that these results are 
                 only part of the overall picture, and a neurologist will need to review them along with your
                 symptoms, medical history, and any other tests. They can explain what the findings might mean 
                 for you, discuss possible next steps, and answer any questions you have. Please schedule a 
                 follow‑up appointment with your neurologist to go over this information in detail.
                 This explanation is for your understanding only and does not replace professional medical 
                 advice."""
                    

)
state = safe_guard_node(state)

print("Safety Passed:", state.safety_passed)
print("Safety Notes:", state.safety_notes)
