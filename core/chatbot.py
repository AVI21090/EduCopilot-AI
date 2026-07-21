import time

from google.api_core.exceptions import ResourceExhausted

from chains.rag_chain import (
    conversational_rag_chain,
    llm,
)


def generate_response(question: str, session_id: str):
    """
    Generates an AI response along with source page numbers.
    """

    try:

        start_time = time.time()

        response = conversational_rag_chain.invoke(
            {"input": question},
            config={
                "configurable": {
                    "session_id": session_id,
                }
            },
        )

        response_time = round(time.time() - start_time, 2)

        answer = response.get("answer", "").strip()

        if not answer:
            answer = (
                "⚠️ I couldn't generate an answer for this question. "
                "Please try asking it differently."
            )

        pages = []

        documents = response.get("context", [])

        for doc in documents:

            page = doc.metadata.get("page")

            if page is not None:
                pages.append(page + 1)

        pages = sorted(set(pages))

        return {
            "answer": answer,
            "pages": pages,
            "response_time": response_time,
            "documents_used": len(documents),
        }

    except ResourceExhausted:

        return {
            "answer": (
                "⚠️ Gemini API quota has been exceeded.\n\n"
                "Please wait until your quota resets "
                "or use another Gemini API key."
            ),
            "pages": [],
            "response_time": 0,
            "documents_used": 0,
        }

    except Exception:

        return {
            "answer": (
                "❌ Something went wrong while generating the response.\n\n"
                "Please try again."
            ),
            "pages": [],
            "response_time": 0,
            "documents_used": 0,
        }


# =====================================================
# Conversation Summary
# =====================================================

def summarize_conversation(chat_history):
    """
    Generates a summary of the conversation.
    """

    if not chat_history:
        return "No conversation available."

    conversation = ""

    for sender, message in chat_history:

        conversation += f"{sender}: {message['answer']}\n"

    prompt = f"""
Summarize the following conversation in 5-8 concise bullet points.

Conversation:
{conversation}
"""

    try:

        response = llm.invoke(prompt)

        return response.content.strip()

    except Exception:

        return "Unable to generate conversation summary."