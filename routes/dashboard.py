from flask import Blueprint, render_template
from models.database import db, Subjects, STUDY_SESSIONS, AIInsight
from datetime import date

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/")
def dashb():
    today_session = STUDY_SESSIONS.query.filter_by(date=date.today()).all()
    upcoming_subjects = Subjects.query.order_by(Subjects.exam_date).all()
    unread_insights = AIInsight.query.filter_by(is_read = False).all()
    return render_template("dashboard.html", today=date.today(), active_page="dashboard", today_sessions = today_session, upcoming_subjects = upcoming_subjects, unread_insights = unread_insights)