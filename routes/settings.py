from flask import render_template, Blueprint, request
from models.database import SETTINGS, db

settings = Blueprint("settings", __name__)

@settings.route("/settings", methods = ["GET", "POST"])
def configuration():
    #GET
    data = SETTINGS.query.filter_by(key = "daily_hours").first()

    if data is None:
        db.session.add(SETTINGS(key = "daily_hours", value = 4.0))
    elif data.value is None:
        data.value = 4.0

    db.session.commit()
    #POST
    user_hours = request.form.get("daily_hours")

    if user_hours is not None:
        data.value = user_hours
        db.session.commit()

    return render_template("settings.html")