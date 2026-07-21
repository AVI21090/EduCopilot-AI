from langchain_core.chat_history import InMemoryChatMessageHistory

# =====================================================
# Chat History Store
# =====================================================

store: dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """
    Returns chat history for the given session.
    Creates a new history if the session doesn't exist.
    """

    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]