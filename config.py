#All configuration variables
from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv()

BASE_DIR = Path(__file__).parent

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_PATH = BASE_DIR / "database" / "study_planner.db"
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
MAX_FILE_SIZE = 25 * 1024 * 1024 #bytes
ALLOWED_EXTENSIONS = {"pdf"}
OLLAMA_MODEL = "gemini-3-flash-preview"
OLLAMA_BASE_URL = r"http://localhost:11434"
