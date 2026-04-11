from pathlib import Path
import os


dir = Path(__file__).parent
os.chdir(dir)

routes = Path("routes")
routes.mkdir(exist_ok=True)

(routes / "__init__.py").touch()
(routes / "dashboard.py").touch()
(routes / "subjects.py").touch()
(routes / "planner.py").touch()
(routes / "progress.py").touch()
(routes / "ai.py").touch()

services = Path("services")
services.mkdir(exist_ok=True)

(services / "__init__.py").touch()
(services / "pdf_service.py").touch()
(services / "planner_service.py").touch()
(services / "scoring_service.py").touch()
(services / "ai_service.py").touch()

models = Path("models")
models.mkdir()

(models / "__init__.py").touch()
(models / "database.py").touch()

utils = Path("utils")
utils.mkdir()

(utils / "__init__.py").touch()
(utils / "text_cleaner.py").touch()
(utils / "chunker.py").touch()

template = Path("templates")
template.mkdir()

(template / "base.html").touch()
(template / "dashboard.html").touch()
(template / "subjects.html").touch()
(template / "calendar.html").touch()
(template / "progress.html").touch()

static = Path("static")
static.mkdir()

(static / "css").mkdir()
(static / "js").mkdir()
(static / "uploads").mkdir()

db = Path("database")
db.mkdir()

(db / "study_planner.db").touch()