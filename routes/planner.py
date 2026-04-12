from flask import Blueprint
from services.planner_service import generate_schedule

planner = Blueprint('planner', __name__)

@planner.route("/plan")
def generate():
    return str(generate_schedule())