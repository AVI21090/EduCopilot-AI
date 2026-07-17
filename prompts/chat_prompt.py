from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

# =====================================================
# History Aware Retriever Prompt
# =====================================================

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Given the chat history and the latest user question,
rewrite the latest question so that it becomes a
standalone question.

Do NOT answer the question.

If the latest question is already standalone,
return it unchanged.
            """,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

# =====================================================
# Chat Prompt
# =====================================================

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are EduCopilot AI.

You are a helpful educational AI assistant.

Answer the user's question ONLY using the provided document context.

Rules:
- Use only the retrieved document context.
- Do not make up information.
- If the answer is not available in the document, reply exactly:
  "I could not find this information in the uploaded PDF."
- Explain concepts in simple language.
- Use bullet points whenever appropriate.
- Keep answers clear and well formatted.

<context>
{context}
</context>
            """,
        ),

        MessagesPlaceholder(variable_name="chat_history"),

        (
            "human",
            "{input}",
        ),
    ]
)