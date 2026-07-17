from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import settings


def split_pdf(pdf):
    """
    Extracts text from the uploaded PDF and splits it
    into smaller chunks for embedding generation.
    """

    text = ""

    for page in pdf.pages:
        extracted_text = page.extract_text()

        if extracted_text:
            text += extracted_text + "\n"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ],
    )

    chunks = splitter.split_text(text)

    return chunks