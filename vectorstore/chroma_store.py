import os
import shutil
import tempfile

import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma

from config.settings import settings
from utils.embeddings import get_embedding_model

embedding_model = get_embedding_model()

DB_PATH = os.path.join(tempfile.gettempdir(), "chroma_db")


def create_vector_store(documents):

    os.makedirs(DB_PATH, exist_ok=True)

    client = chromadb.PersistentClient(
        path=DB_PATH,
        settings=Settings(anonymized_telemetry=False),
    )

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        client=client,
        collection_name=settings.COLLECTION_NAME,
    )

    return vector_store


def load_vector_store():

    if not os.path.isdir(DB_PATH):
        return None

    client = chromadb.PersistentClient(
        path=DB_PATH,
        settings=Settings(anonymized_telemetry=False),
    )

    return Chroma(
        client=client,
        collection_name=settings.COLLECTION_NAME,
        embedding_function=embedding_model,
    )


def get_retriever():

    vector_store = load_vector_store()

    if vector_store is None:
        raise Exception("Vector store not found. Please upload a PDF first.")

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

    os.makedirs(DB_PATH, exist_ok=True)

    return True