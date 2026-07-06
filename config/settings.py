import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Settings:
    """
    Stores all project configuration variables.
    """

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


settings = Settings()