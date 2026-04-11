from flask import Blueprint
from datetime import date, datetime
from models.database import db,Subjects


subjects = Blueprint('subjects', __name__)

@subjects.route("/test")
def test():
    new_subject = Subjects(
    name="Mathematics",
    exam_date=date(2025, 6, 15),
    objective_difficulty=0.8,
    passion_level=0.9,
    effective_difficulty=0.88,
    importance_weight=2.5,
    progress=0.10,
    created_at=datetime.utcnow()
)

    db.session.add(new_subject)
    db.session.commit()
    return "Math added"