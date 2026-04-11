from pathlib import Path
import os


dir = Path(__file__).parent
os.chdir(dir)

db = Path("database")
db.mkdir()

(db / "study_planner.db").touch()