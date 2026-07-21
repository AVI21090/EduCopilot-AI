from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import settings


def get_embedding_model():
    """
    Returns the HuggingFace embedding model.
    """

    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )