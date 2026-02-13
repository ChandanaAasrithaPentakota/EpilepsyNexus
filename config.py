import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
HF_TOKEN=os.getenv("HF_TOKEN")
OLLAMA_API_KEY=os.getenv("OLLAMA_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")