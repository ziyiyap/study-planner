from flask import Blueprint, render_template
from models.database import db, STUDY_SESSIONS, Subjects
from datetime import date, timedelta

calendar = Blueprint("calendar", __name__)

@calendar.route("/calendar", methods = ["GET"])
def calendar_page():
    monday = date.today() - timedelta(days=date.today().weekday())

    week_dates = []

    for i in range(7):
        week_dates.append(monday + timedelta(days=i))

    sessions_by_day = []

    for dates in week_dates:
        result = STUDY_SESSIONS.query.filter_by(date=dates).all()
        sessions_by_day.append(result)

    subjects_map = {s.id: s.name for s in Subjects.query.all()}
    return render_template("calendar.html", subjects_map = subjects_map, week_dates = week_dates, sessions_by_day = sessions_by_day, active_page = "calendar")