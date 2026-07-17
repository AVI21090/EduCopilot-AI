from langchain_huggingface import HuggingFaceEmbeddings

from config.settings import settings


def get_embedding_model():
    """
    Returns the HuggingFace embedding model.
    """

    embedding_model = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL
    )

    return embedding_model