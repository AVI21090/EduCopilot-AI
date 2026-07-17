from langchain_chroma import Chroma

from config.settings import settings
from utils.embeddings import get_embedding_model


def create_vector_store(chunks):
    """
    Creates and stores document embeddings in ChromaDB.
    """

    embedding_model = get_embedding_model()

    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        persist_directory=settings.CHROMA_DB_PATH,
        collection_name=settings.COLLECTION_NAME,
    )

    return vector_store


def load_vector_store():
    """
    Loads the existing ChromaDB vector store.
    """

    embedding_model = get_embedding_model()

    vector_store = Chroma(
        persist_directory=settings.CHROMA_DB_PATH,
        embedding_function=embedding_model,
        collection_name=settings.COLLECTION_NAME,
    )

    return vector_store


def get_retriever():
    """
    Returns a retriever for semantic search.
    """

    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": settings.RETRIEVER_K
        }
    )

    return retriever