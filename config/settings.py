import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Stores all project configuration variables.
    """

    # Google Gemini
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Lite model uses less quota than flash
    MODEL_NAME = "gemini-2.5-flash-lite"

    TEMPERATURE = 0

    # Embedding Model
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    # Text Splitter
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # ChromaDB
    CHROMA_DB_PATH = "chroma_db"
    COLLECTION_NAME = "educopilot"
    RETRIEVER_K = 3


settings = Settings()