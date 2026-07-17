from vectorstore.chroma_store import get_retriever


def retrieve_documents(query: str):
    """
    Retrieve the most relevant documents from ChromaDB.
    """

    retriever = get_retriever()

    docs = retriever.invoke(query)

    return docs