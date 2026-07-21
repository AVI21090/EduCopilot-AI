from pypdf import PdfReader


# =====================================================
# PDF Loader
# =====================================================

def load_pdf(uploaded_file):
    """
    Safely loads an uploaded PDF file.
    """

    try:

        pdf = PdfReader(uploaded_file)

        if not pdf.pages:
            raise ValueError("The uploaded PDF contains no pages.")

        return pdf

    except Exception as e:

        raise ValueError(
            f"Unable to read the uploaded PDF: {str(e)}"
        )