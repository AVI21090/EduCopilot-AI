import os
import shutil
import tempfile

from langchain_chroma import Chroma

from config.settings import settings
from utils.embeddings import get_embedding_model

embedding_model = get_embedding_model()

# Streamlit Cloud ke liye writable directory
DB_PATH = os.path.join(tempfile.gettempdir(), "chroma_db")


def create_vector_store(documents):
    if os.path.exists(DB_PATH):
        vector_store = load_vector_store()
        vector_store.add_documents(documents)
    else:
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embedding_model,
            persist_directory=DB_PATH,
            collection_name=settings.COLLECTION_NAME,
        )
    return vector_store


def load_vector_store():
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_model,
        collection_name=settings.COLLECTION_NAME,
    )


def get_retriever():
    vector_store = load_vector_store()

    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": settings.RETRIEVER_K,
            "fetch_k": settings.FETCH_K,
            "lambda_mult": settings.LAMBDA_MULT,
        },
    )


def clear_vector_store():
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)
    return True