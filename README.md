# EpilepsyNexus: An Agentic AI Framework with a RAG-Driven Diagnostic System for MRI- and EEG-Based Epilepsy Screening

EpilepsyNexus is an end-to-end multimodal clinical decision support
system that integrates **MRI imaging, EEG analysis, clinical symptoms,
and medical knowledge retrieval** to assist in epilepsy evaluation.\
The system produces both **neurologist-style structured reports** and
**patient-friendly explanations**, while ensuring safety and medical
neutrality.

------------------------------------------------------------------------

## 🚀 Project Overview

Epilepsy diagnosis often requires integrating multiple modalities such
as: - Neuroimaging (MRI) - Electrophysiology (EEG) - Clinical history
and symptoms - Medical guidelines and evidence

EpilepsyNexus combines these using a **LangGraph-based modular AI
pipeline** with: - Machine learning models - Large Language Models
(LLMs) - Retrieval-Augmented Generation (RAG) - Safety and
explainability layers

------------------------------------------------------------------------

## 🏗️ System Architecture

The pipeline follows this multimodal flow:

1.  MRI Preprocessing & Classification
2.  EEG Classification
3.  MRI + EEG + Symptoms Fusion
4.  Medical RAG for grounded knowledge
5.  Neurologist-style Diagnostic Report
6.  Patient Communication
7.  Safety Guard for medical neutrality

------------------------------------------------------------------------

## 🧩 Key Features

✅ Multimodal epilepsy reasoning\
✅ Structured clinical output\
✅ Evidence-grounded RAG\
✅ Safety and hallucination control\
✅ Patient-friendly explanations\
✅ Modular and extensible design\
✅ Research and deployment ready

------------------------------------------------------------------------

## 📁 Project Structure

```
EpilepsyNexus/
│
├── llms/
│   ├── __init__.py
│   └── groq_llm.py
│
├── models/
│   ├── __init__.py
│   ├── efficientnet_transfer_learning.h5
│   ├── efficientnet_v2_finetuned.h5
│   ├── lightgbm.pkl
│   └── mri_efficient.h5
│
├── nodes/
│   ├── __init__.py
│   ├── eeg_classifier.py
│   ├── medical_rag.py
│   ├── mri_classifier.py
│   ├── mri_eeg_combiner.py
│   ├── neuro_diagnostic_report.py
│   ├── patient_communication.py
│   └── safe_guard.py
│
├── prompts/
│   ├── medical_rag_prompt.txt
│   ├── mri_eeg_combiner_prompt.txt
│   ├── neuro_diagnostic_report_prompt.txt
│   ├── patient_communication_prompt.txt
│   └── safe_guard_prompt.txt
│
├── trails/                # Experimental notebooks and vector DB setup
│
├── build_graph.py         # Graph construction and workflow definition
├── graph.py               # State and LangGraph pipeline
├── main.py                # CLI entry point
├── config.py              # API keys and configuration
├── template.py            # Project template utilities
├── sample.txt             # Sample EEG input
│
├── requirements.txt
├── .gitignore
└── README.md
```

------------------------------------------------------------------------

## ⚙️ Installation

### 1️⃣ Clone the repository

``` bash
git clone https://github.com/yourusername/EpilepsyNexus.git
cd EpilepsyNexus
```

### 2️⃣ Create virtual environment

Create and activate a virtual environment to manage project dependencies.

#### 🐧 Linux / Mac

```bash
python -m venv venv
source venv/bin/activate
```

#### 🪟 Windows (Command Prompt)

```bash
python -m venv venv
venv\Scripts\activate
```

#### 🪟 Windows (PowerShell)

```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3️⃣ Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🔑 Environment Setup

Create a `.env` file:

    GROQ_API_KEY=your_groq_key
    PINECONE_API_KEY=your_pinecone_key

------------------------------------------------------------------------

## ▶️ Running the System

Run using command line:

``` bash
python main.py --mri path_to_mri_image --eeg path_to_eeg_file --symptoms "Patient symptom description"
```

------------------------------------------------------------------------

## 📊 Output

The system generates:

-   Epilepsy presence (yes / uncertain)
-   Seizure type
-   Seizure phase
-   Multimodal explanation
-   Medical knowledge grounding
-   Structured neurologist report
-   Patient-friendly explanation
-   Safety validation

------------------------------------------------------------------------

## 🧪 Example Use Cases

-   Clinical decision support
-   Medical AI research
-   Multimodal LLM evaluation
-   Epilepsy education tools
-   Explainable healthcare AI

------------------------------------------------------------------------

## ⚠️ Disclaimer

This system is for **research and educational purposes only**.\
It is not intended for clinical diagnosis or treatment.\
All outputs must be reviewed by qualified healthcare professionals.

------------------------------------------------------------------------

## 📌 Future Work

-   Confidence scoring
-   Uncertainty estimation
-   Structured symptom extraction
-   Clinical dataset validation
-   Mobile and web interfaces
-   Real-time EEG integration

------------------------------------------------------------------------

## 🤝 Contributions

Contributions and suggestions are welcome.\
Please open an issue or submit a pull request.
