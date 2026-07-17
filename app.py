import uuid
import streamlit as st

from core.chatbot import generate_response
from utils.pdf_loader import load_pdf
from utils.text_splitter import split_pdf
from vectorstore.chroma_store import create_vector_store

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="EduCopilot AI",
    page_icon="🎓",
    layout="wide",
)

# =====================================================
# Session ID
# =====================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.title("🎓 EduCopilot AI")
st.caption("Phase 9 - Conversational RAG")

# =====================================================
# PDF Upload
# =====================================================

uploaded_pdf = st.file_uploader(
    "📄 Upload PDF",
    type=["pdf"],
)

if uploaded_pdf is not None:

    with st.spinner("📖 Reading PDF..."):
        pdf = load_pdf(uploaded_pdf)

    st.success(f"✅ PDF Uploaded Successfully ({len(pdf.pages)} pages)")

    with st.spinner("✂️ Splitting PDF..."):
        chunks = split_pdf(pdf)

    st.info(f"📚 Total Chunks Created: {len(chunks)}")

    with st.spinner("🧠 Creating ChromaDB..."):
        create_vector_store(chunks)

    st.success("✅ ChromaDB Ready!")

# =====================================================
# Chat
# =====================================================

st.divider()

st.subheader("💬 Chat with EduCopilot AI")

question = st.text_input("Ask your question")

if st.button("Generate Response", use_container_width=True):

    if question.strip():

        with st.spinner("🤖 Thinking..."):

            response = generate_response(
                question,
                st.session_state.session_id,
            )

        st.success(response)

    else:

        st.warning("⚠ Please enter a question.")