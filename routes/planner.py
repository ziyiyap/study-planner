from flask import Blueprint, request, jsonify, redirect, url_for
from services.planner_service import generate_schedule
from models.database import db, STUDY_SESSIONS

planner = Blueprint('planner', __name__)

@planner.route("/plan", methods = ["GET"])
def generate():
    generate_schedule()
    return redirect(url_for("dashboard.dashb"))
    
@planner.route("/planner/update_session", methods = ["POST"])
def update_plan():
    data = request.get_json()

    session_id, status = data['session_id'], data['status']

    result = STUDY_SESSIONS.query.get(session_id)

    if result is None:
        return jsonify({"success": False})
    
    result.status = status

    db.session.commit()

    return jsonify({"success": True})