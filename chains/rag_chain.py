from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import settings
from memory.chat_memory import get_session_history
from prompts.chat_prompt import (
    chat_prompt,
    contextualize_q_prompt,
)
from vectorstore.chroma_store import get_retriever

print("API Key Loaded:", bool(settings.GOOGLE_API_KEY))
print("Model:", settings.MODEL_NAME)
llm = ChatGoogleGenerativeAI(
    model=settings.MODEL_NAME,
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0,
    timeout=180,
    max_retries=2,
)


def get_conversational_chain():

    retriever = get_retriever()

    history_aware_retriever = create_history_aware_retriever(
        llm=llm,
        retriever=retriever,
        prompt=contextualize_q_prompt,
    )

    document_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=chat_prompt,
    )

    rag_chain = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=document_chain,
    )

    return RunnableWithMessageHistory(
        runnable=rag_chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )