import uuid
import streamlit as st

from assets.styles import load_css

from core.chatbot import (
    generate_response,
    summarize_conversation,
)
from utils.pdf_loader import load_pdf
from utils.text_splitter import split_pdf
from vectorstore.chroma_store import (
    create_vector_store,
    clear_vector_store,
)

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="EduCopilot AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()


# =====================================================
# Session State
# =====================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_pdfs" not in st.session_state:
    st.session_state.uploaded_pdfs = []

# =====================================================
# Hero Header
# =====================================================

st.markdown("""
<div class="hero">

<div style="display:flex;
align-items:center;
justify-content:space-between;
gap:20px;
flex-wrap:wrap;">

<div>

<h1 style="margin-bottom:8px;">
🎓 EduCopilot AI
</h1>

<p style="font-size:18px;margin:0;">
Professional Conversational RAG System
</p>

<p style="margin-top:8px;">
🚀 Gemini • LangChain • ChromaDB • HuggingFace
</p>

</div>

<div style="
font-size:70px;
">
🤖
</div>

</div>

</div>
""",unsafe_allow_html=True)
# =====================================================
# Dashboard
# =====================================================

status = "🟢 Ready" if st.session_state.pdf_uploaded else "🟡 Waiting"

c1,c2,c3=st.columns(3)

cards=[
("📄 PDFs",len(st.session_state.uploaded_pdfs)),
("💬 Chats",len(st.session_state.chat_history)//2),
("🤖 Status",status)
]

for col,(title,value) in zip((c1,c2,c3),cards):

    with col:

        st.markdown(f"""

<div class="metric-card">

<div class="metric-number">

{value}

</div>

<div class="metric-title">

{title}

</div>

</div>

""",unsafe_allow_html=True)

st.write("")

# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.markdown("## 🎓 EduCopilot AI")
    st.caption("Your Intelligent PDF Assistant")
    if st.session_state.pdf_uploaded:
        st.success("🟢 AI Ready")
    else:
        st.warning("🟡 Waiting for PDFs")

    st.divider()

    # ---------------- Upload PDFs ---------------- #

    st.subheader("📄 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Choose one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )

if uploaded_files:

    try:

        progress = st.progress(0)

        total = len(uploaded_files)

        for index, file in enumerate(uploaded_files, start=1):

            with st.spinner(f"Processing {file.name}"):

                pdf = load_pdf(file)

                docs = split_pdf(pdf, file.name)

                create_vector_store(docs)

                progress.progress(index / total)

        st.session_state.pdf_uploaded = True

        st.session_state.uploaded_pdfs = [
            file.name for file in uploaded_files
        ]

        st.success(f"✅ {total} PDF(s) uploaded successfully!")

    except Exception as e:

        st.error(str(e))
    
    st.divider()

    # ---------------- Knowledge Base ---------------- #

    st.subheader("📚 Uploaded PDFs")

    if st.session_state.uploaded_pdfs:

        for pdf in st.session_state.uploaded_pdfs:

            st.success(f"📄 {pdf}")

    else:

        st.info("No PDFs Uploaded")

    st.divider()

    # ---------------- Actions ---------------- #

    st.subheader("⚙ Controls")

    if st.button("🗑 Clear Chat", use_container_width=True):

        st.session_state.chat_history = []

        st.session_state.session_id = str(uuid.uuid4())

        st.success("Chat Cleared")

    if st.button("🗑 Clear Knowledge Base", use_container_width=True):

        if clear_vector_store():

            st.session_state.chat_history = []

            st.session_state.uploaded_pdfs = []

            st.session_state.pdf_uploaded = False

            st.session_state.session_id = str(uuid.uuid4())

            st.success("Knowledge Base Cleared")

            st.rerun()

        else:

            st.info("Knowledge Base already empty.")

    st.divider()

       # ---------------- About ---------------- #

    st.subheader("ℹ About")

    st.info("""
### 🎓 EduCopilot AI

Professional Conversational RAG Assistant

### ⚙ Tech Stack

• Gemini

• LangChain

• ChromaDB

• HuggingFace

• Streamlit
""")

# =====================================================
# Main Chat
# =====================================================

st.subheader("💬 Ask Anything From Your PDFs")

if not st.session_state.chat_history:

    st.info("""
👋 Welcome to EduCopilot AI

📄 Upload your PDFs from the sidebar.

💬 Ask questions in the chat box below.

🤖 AI will answer using your uploaded documents.
""")

question = st.chat_input("Ask anything from your PDFs...")
if question:

    if not st.session_state.pdf_uploaded:

        st.warning("Please upload a PDF first.")

    else:

        with st.spinner("🤖 Thinking..."):

            response=generate_response(
                question,
                st.session_state.session_id,
            )

        st.session_state.chat_history.append(
            (
                "You",
                {
                    "answer":question,
                    "pages":[]
                }
            )
        )

        st.session_state.chat_history.append(
            (
                "EduCopilot AI",
                response
            )
        )

# =====================================================
# Conversation
# =====================================================

if st.session_state.chat_history:

    st.divider()

    st.markdown("## 💬 Conversation")

    for sender, message in st.session_state.chat_history:

        if sender == "You":

            with st.chat_message("user", avatar="🧑‍💻"):

                st.markdown(message["answer"])

        else:

            with st.chat_message("assistant", avatar="🤖"):

                st.markdown(message["answer"])

                st.caption("✨ Generated by EduCopilot AI")

                if message.get("pages"):

                    badges = ""

                    for page in message["pages"]:

                        badges += f"""
                        <span style="
                        display:inline-block;
                        background:#2563eb;
                        color:white;
                        padding:5px 12px;
                        border-radius:20px;
                        margin-right:6px;
                        margin-top:5px;
                        font-size:12px;
                        font-weight:600;
                        ">
                        📄 Page {page}
                        </span>
                        """

                    st.markdown(
                        badges,
                        unsafe_allow_html=True,
                    )

                if message.get("response_time"):

                    st.caption(
                        f"⚡ Response Time : {message['response_time']} sec"
                    )

                if message.get("documents_used"):

                    st.caption(
                        f"📚 Documents Used : {message['documents_used']}"
                    )

# =====================================================
# Retrieval Statistics
# =====================================================

# =====================================================
# Retrieval Statistics
# =====================================================

if st.session_state.chat_history:

    last_sender, last_message = st.session_state.chat_history[-1]

    if (
        last_sender == "EduCopilot AI"
        and "response_time" in last_message
    ):

        st.divider()

        st.markdown("## 📊 Retrieval Statistics")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                label="⚡ Response Time",
                value=f"{last_message['response_time']} sec",
            )

        with c2:

            st.metric(
                label="📚 Documents Used",
                value=last_message["documents_used"],
            )   

# =====================================================
# AI Conversation Summary
# =====================================================

if st.session_state.chat_history:

    st.divider()

    st.markdown("## 📝 AI Conversation Summary")

    if st.button(
        "🧠 Generate AI Summary",
        use_container_width=True,
    ):

        with st.spinner("Generating summary..."):

            summary = summarize_conversation(
                st.session_state.chat_history
            )

        st.success("✅ Summary Generated!")

        st.info(summary)

# =====================================================
# Download Conversation
# =====================================================

if st.session_state.chat_history:

    st.divider()

    st.markdown("## 📥 Export Conversation")

    conversation = ""

    for sender, message in st.session_state.chat_history:

        conversation += f"{sender}\n"
        conversation += "-" * len(sender) + "\n"
        conversation += message["answer"]
        conversation += "\n\n"

    st.download_button(
        label="⬇ Download Chat (.txt)",
        data=conversation,
        file_name="educopilot_chat.txt",
        mime="text/plain",
        use_container_width=True,
    )

# =====================================================
# Footer
# =====================================================

st.divider()

st.markdown(
    """
    <div class="footer">

        <h3>🎓 EduCopilot AI</h3>

        <p>
            Professional Conversational RAG Assistant
        </p>

        <p>
            🚀 Powered by
            <b>Gemini • LangChain • ChromaDB • HuggingFace</b>
        </p>

        <p>
            Made with ❤️ using Streamlit
        </p>

        <hr style="margin:15px 0;">

        <p style="font-size:14px;color:#6b7280;">
            © 2026 EduCopilot AI | Intelligent PDF Chat Assistant
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)