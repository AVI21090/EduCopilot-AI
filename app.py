import streamlit as st
from core.chatbot import generate_response

st.set_page_config(
    page_title="EduCopilot AI",
    page_icon="🎓",
)

st.title("🎓 EduCopilot AI")
st.write("Phase 2 - Prompt Templates")

question = st.text_input("Ask me anything")

if st.button("Generate Response"):
    if question.strip():
        response = generate_response(question)
        st.success(response)
    else:
        st.warning("Please enter a question.")