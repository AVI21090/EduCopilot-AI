import os
import shutil

from langchain_chroma import Chroma

from config.settings import settings
from utils.embeddings import get_embedding_model


# =====================================================
# Shared Embedding Model
# =====================================================

embedding_model = get_embedding_model()


# =====================================================
# Create / Update Vector Store
# =====================================================

def create_vector_store(documents):
    """
    Creates a new ChromaDB or adds new documents
    to the existing vector store.
    """

    if os.path.exists(settings.CHROMA_DB_PATH):

        vector_store = load_vector_store()
        vector_store.add_documents(documents)

    else:

        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embedding_model,
            persist_directory=settings.CHROMA_DB_PATH,
            collection_name=settings.COLLECTION_NAME,
        )

    return vector_store


# =====================================================
# Load Vector Store
# =====================================================

def load_vector_store():
    """
    Loads the existing ChromaDB database.
    """

    return Chroma(
        persist_directory=settings.CHROMA_DB_PATH,
        embedding_function=embedding_model,
        collection_name=settings.COLLECTION_NAME,
    )


# =====================================================
# Retriever
# =====================================================

def get_retriever():
    """
    Returns an optimized MMR retriever.
    """

    vector_store = load_vector_store()

    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": settings.RETRIEVER_K,
            "fetch_k": settings.FETCH_K,
            "lambda_mult": settings.LAMBDA_MULT,
        },
    )


# =====================================================
# Clear Vector Store
# =====================================================

def clear_vector_store():
    """
    Deletes the complete ChromaDB database.
    """

    if not os.path.exists(settings.CHROMA_DB_PATH):
        return False

    shutil.rmtree(settings.CHROMA_DB_PATH)

    return True