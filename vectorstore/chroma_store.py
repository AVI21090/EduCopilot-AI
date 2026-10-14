
import os
import shutil

import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma

from config.settings import settings
from utils.embeddings import get_embedding_model


DB_PATH = settings.CHROMA_DB_PATH


def get_chroma_client():
    os.makedirs(DB_PATH, exist_ok=True)

    return chromadb.PersistentClient(
        path=DB_PATH,
        settings=Settings(anonymized_telemetry=False),
    )


def create_vector_store(documents):
    if not documents:
        raise ValueError("No documents provided to create the vector store.")

    client = get_chroma_client()

    vector_store = Chroma(
        client=client,
        collection_name=settings.COLLECTION_NAME,
        embedding_function=get_embedding_model(),
    )

    vector_store.add_documents(documents)

    return vector_store


def load_vector_store():
    if not os.path.isdir(DB_PATH):
        return None

    client = get_chroma_client()

    try:
        collection = client.get_collection(
            name=settings.COLLECTION_NAME
        )

        if collection.count() == 0:
            return None

    except Exception:
        return None

    return Chroma(
        client=client,
        collection_name=settings.COLLECTION_NAME,
        embedding_function=get_embedding_model(),
    )


def get_retriever():
    vector_store = load_vector_store()

    if vector_store is None:
        raise RuntimeError(
            "Vector store not found or empty. Please upload a PDF first."
        )

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
