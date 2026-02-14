import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate
from graph import EpilepsyState
from llms.groq_llm import get_groq_llm
from config import PINECONE_API_KEY

prompt_path = PROJECT_ROOT / "prompts" / "medical_rag_prompt.txt"

with open(prompt_path, "r", encoding="utf-8") as f:
    template_text = f.read()

prompt = PromptTemplate(
    template=template_text,
    input_variables=[
        "context",
        "epilepsy_presence",
        "seizure_phase",
        "seizure_type",
        "fusion_explanation",
    ],
)

INDEX_NAME = "epilepsynexus"

pc = Pinecone(api_key=PINECONE_API_KEY)

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",
    encode_kwargs={"normalize_embeddings": True}
)

vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embedding_model,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})


llm = get_groq_llm()

def medical_rag_node(state: EpilepsyState) -> EpilepsyState:
    """
    Retrieves epilepsy knowledge and enriches model outputs.
    """

    # Build retrieval query
    query = f"""
    Epilepsy Presence: {state.epilepsy_presence}
    Seizure Phase: {state.seizure_phase}
    Seizure Type: {state.seizure_type}
    """

    # Retrieve documents from Pinecone
    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    # Run Groq LLM
    response = llm.invoke(
        prompt.format(
            context=context,
            epilepsy_presence=state.epilepsy_presence,
            seizure_phase=state.seizure_phase,
            seizure_type=state.seizure_type,
            fusion_explanation=state.fusion_explanation,
        )
    )

    # Store in state
    state.medical_context = response.content

    return state

