from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import settings
from prompts.chat_prompt import (
    chat_prompt,
    contextualize_q_prompt,
)
from vectorstore.chroma_store import get_retriever

# =====================================================
# Gemini LLM
# =====================================================

llm = ChatGoogleGenerativeAI(
    model=settings.MODEL_NAME,
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=settings.TEMPERATURE,
)

# =====================================================
# Base Retriever
# =====================================================

retriever = get_retriever()

# =====================================================
# History Aware Retriever
# =====================================================

history_aware_retriever = create_history_aware_retriever(
    llm=llm,
    retriever=retriever,
    prompt=contextualize_q_prompt,
)

# =====================================================
# Document Chain
# =====================================================

document_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=chat_prompt,
)

# =====================================================
# Conversational Retrieval Chain
# =====================================================

rag_chain = create_retrieval_chain(
    retriever=history_aware_retriever,
    combine_docs_chain=document_chain,
)

# =====================================================
# Chat History Store
# =====================================================

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# =====================================================
# Conversational RAG Chain
# =====================================================

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)