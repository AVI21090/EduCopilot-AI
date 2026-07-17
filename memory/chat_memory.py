from langchain_core.chat_history import InMemoryChatMessageHistory

# ==========================================================
# In-Memory Chat Store
# ==========================================================
# Stores chat history for every user session.
# Later we can replace this with Redis, MongoDB, or PostgreSQL
# without changing the chatbot code.
# ==========================================================

store = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """
    Returns the chat history for the given session.

    If the session does not exist,
    a new chat history is created automatically.
    """

    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]