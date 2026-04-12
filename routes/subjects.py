from flask import Blueprint
from datetime import date, datetime
from models.database import db,Subjects
from services.scoring_service import get_all_priorities


subjects = Blueprint('subjects', __name__)

@subjects.route("/all_priorities")
def priorities():
    return str(get_all_priorities())

@subjects.route("/subjects/create")
def create():
    math = Subjects(
    name="Math",
    exam_date=date(2026, 6, 15),
    objective_difficulty=0.8,
    passion_level=0.9,
    effective_difficulty=0.88,
    importance_weight=2.5,
    progress=0.10,
    created_at=datetime.now()
)
    
    physical_chem = Subjects(
    name="Physical Chemistry",
    exam_date=date(2026, 7, 15),
    objective_difficulty=0.8,
    passion_level=0.7,
    effective_difficulty=0.7,
    importance_weight=2.5,
    progress=0.60,
    created_at=datetime.now()
)
    
    db.session.add(math)
    db.session.add(physical_chem)
    db.session.commit()

    return "Math created!\nPhysical Chemistry created!"