from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import settings
from prompts.chat_prompt import chat_prompt


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0.7,
)


def generate_response(question: str):

    chain = chat_prompt | llm

    response = chain.invoke(
        {
            "question": question,
        }
    )

    return response.content