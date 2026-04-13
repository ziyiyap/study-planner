from flask import Blueprint, render_template
from models.database import db, Subjects, STUDY_SESSIONS
from datetime import date

progress = Blueprint('progress', __name__)

@progress.route("/progress", methods = ["GET"])
def query_progress():
    all_subjects = Subjects.query.all()
    total_session = STUDY_SESSIONS.query.count()
    completed_sessions = STUDY_SESSIONS.query.filter_by(status = "completed").count()
    missing_sessions = STUDY_SESSIONS.query.filter_by(status = "missed").count()
    recent_ten = STUDY_SESSIONS.query.order_by(STUDY_SESSIONS.date.desc()).limit(10).all()

    subject_map = {s.id : s.name for s in Subjects.query.all()}
    return render_template("progress.html",
        subjects=all_subjects,
        subjects_map = subject_map,
        today=date.today(),
        total_sessions=total_session,
        completed_sessions=completed_sessions,
        missed_sessions=missing_sessions,
        recent_sessions=recent_ten,
        active_page="progress"
    )