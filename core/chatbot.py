from chains.rag_chain import conversational_rag_chain

# =====================================================
# Generate Response
# =====================================================

def generate_response(question: str, session_id: str) -> str:
    """
    Generates response using the Conversational
    RAG Chain with chat history.
    """

    response = conversational_rag_chain.invoke(
        {"input": question},
        config={
            "configurable": {
                "session_id": session_id
            }
        }
    )

    # Debug Output
    print("\n========== FULL RESPONSE ==========")
    print(response)
    print("===================================\n")

    return response["answer"]