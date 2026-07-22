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

        print("STEP 1: Calling RAG Chain...")

        response = conversational_rag_chain.invoke(
            {"input": question},
            config={
                "configurable": {
                    "session_id": session_id,
                }
            },
        )

        print("STEP 2: RAG Chain Finished")

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