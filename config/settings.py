```python
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Stores all project configuration variables.
    """

    # Application
    APP_NAME = "EduCopilot AI"
    APP_VERSION = "1.0.0"

    # Gemini
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = "gemini-3.8-flash"
    TEMPERATURE = 0

    # Embedding Model
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    # Text Splitter
    CHUNK_SIZE = 600
    CHUNK_OVERLAP = 100

    # ChromaDB
    CHROMA_DB_PATH = os.path.join(
        tempfile.gettempdir(),
        "chroma_db"
    )
    COLLECTION_NAME = "educopilot"

    # Retriever
    RETRIEVER_K = 3
    FETCH_K = 10
    LAMBDA_MULT = 0.5
    SCORE_THRESHOLD = 0.30

    # UI
    MAX_CHAT_HISTORY = 50
    SHOW_SOURCE_PAGES = True
    SHOW_WELCOME_MESSAGE = True


settings = Settings()
```
