from flask import Blueprint
from datetime import date, datetime
from models.database import db,Subjects
from services.scoring_service import get_all_priorities


subjects = Blueprint('subjects', __name__)
