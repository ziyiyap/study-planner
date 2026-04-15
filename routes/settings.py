from flask import render_template, Blueprint, request, redirect, url_for
from models.database import SETTINGS, db
import config

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/settings", methods = ["GET", "POST"])
def configuration():
    if request.method == "POST":
        user_hours = float(request.form.get("daily_hours"))

        data = SETTINGS.query.get("daily_hours")
        if data:
            data.value = user_hours
        else:
            db.session.add(SETTINGS(key='daily_hours', value = user_hours))
        db.session.commit()
        return redirect(url_for("planner.generate"))
    elif request.method == "GET":
        db_hours = SETTINGS.query.get("daily_hours")
        if db_hours is None:
            db.session.add(SETTINGS(key="daily_hours", value = 4.0))
            db.session.commit()
        db_hours = SETTINGS.query.get("daily_hours")
        return render_template("settings.html", current_daily_hours = db_hours.value, ollama_model = config.OLLAMA_MODEL, active_page = "settings")