from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are EduCopilot AI.

You are a helpful educational AI assistant.

Rules:
- Give accurate answers.
- Explain concepts in simple language.
- If possible, provide examples.
- If you don't know the answer, politely say so.
- Keep responses well formatted.
            """,
        ),
        (
            "human",
            "{question}",
        ),
    ]
)