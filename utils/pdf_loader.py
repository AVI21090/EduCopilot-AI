from pypdf import PdfReader


def load_pdf(uploaded_file):
    """
    Loads the uploaded PDF and returns a PdfReader object.
    """

    pdf = PdfReader(uploaded_file)

    return pdf