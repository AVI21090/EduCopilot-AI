from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import settings


# =====================================================
# PDF Text Splitter
# =====================================================

def split_pdf(pdf, filename="Unknown PDF"):
    """
    Extracts text page-wise, splits it into chunks,
    and attaches metadata for retrieval.
    """

    documents = []

    for page_number, page in enumerate(pdf.pages):

        text = page.extract_text()

        if not text or not text.strip():
            continue

        documents.append(
            Document(
                page_content=text.strip(),
                metadata={
                    "source": filename,
                    "page": page_number,
                },
            )
        )

    if not documents:
        raise ValueError(
            "No readable text found in the uploaded PDF."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(documents)

    # Add Chunk IDs
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = index

    return chunks