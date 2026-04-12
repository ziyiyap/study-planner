from models.database import db, STUDY_SESSIONS, Subjects, SETTINGS
from services.scoring_service import get_all_priorities
from datetime import date, timedelta

def get_daily_hours():
    result = SETTINGS.query.filter_by(key = "daily_hours").first()
    if result is None:
        return 4.0
    return float(result.value)

def allocate_time(priorities, daily_hours): #priorities = get_all_priorities()
    all_allocated_hours = []
    score_sum = sum(t[1] for t in priorities)

    if score_sum == 0:
        return [] # calculate_priority() returned 0, user has no upcoming schedules
    
    for t in priorities:
        allocate_formula = daily_hours * (t[1] / score_sum)
        allocated_hours = max(allocate_formula, 0.5) #minimum study time of 30 minutes

        all_allocated_hours.append([t[0], allocated_hours])

    remaining_hours = daily_hours - sum(alloc[1] for alloc in all_allocated_hours)

    all_allocated_hours[0][1] += remaining_hours

    return all_allocated_hours

def generate_schedule(days = 7):

    for day in range(days):
        for t in allocate_time(get_all_priorities(), get_daily_hours()):
            subject_session = STUDY_SESSIONS(
                subject_id = t[0].id,
                date = date.today() + timedelta(days=day),
                allocated_hours = t[1]
            )
            
            db.session.add(subject_session)

    db.session.commit()