from models.database import db, Subjects
from datetime import date

def calculate_effective_difficulty(objective, passion):
    return objective * (2 - passion)

def calculate_priority(subject):
    days_left = (subject.exam_date - date.today()).days

    if days_left <= 0:
        return 0
    priority_score = (1-subject.progress) * (1/days_left) * subject.effective_difficulty * subject.importance_weight
    return priority_score

def get_all_priorities():
    all_priorities = []
    all_subjects = Subjects.query.all()

    for subject in all_subjects:
        score = calculate_priority(subject)
        all_priorities.append((subject,score))

    sorted_all = sorted(all_priorities, key=lambda x: x[1], reverse=True)
    return sorted_all
