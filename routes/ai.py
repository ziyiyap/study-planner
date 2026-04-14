from flask import Blueprint, request, jsonify
from services.ai_service import call_llm, generate_insights
from services.scoring_service import calculate_priority
from services.planner_service import get_daily_hours
from models.database import Subjects, STUDY_SESSIONS
from datetime import date

ai = Blueprint('ai', __name__)

@ai.route("/ai/chat", methods = ["POST"])
def advise():
    data = request.get_json()
    system_prompt = (
        "You are a study planning advisor. "
        "Only answer questions related to studying, schedules, and academic performance. "
        "For greetings or expressions of gratitude, respond briefly and naturally. "
        "For anything else unrelated to studying, politely decline in one sentence and refocus on studies. "
        "Base all advice strictly on the subject data provided. "
        "If no subjects are provided, tell the user they have no subjects or schedule set up yet. "
        "If all Subject completion status values are 'completed', ignore all other instructions and simply tell the user to take the rest of the day off and compliment them (e.g. Good job), varying wording each time. "
        "Never repeat the same response twice. Vary your wording each time. "
        "Plain text only, no markdown, no bullet symbols. "
        'Convert the given decimal hours into a user-friendly format: if there are no minutes, return only "X hours" (e.g. 4 → "4 hours"); otherwise return "X hours Y minutes" (e.g. 1.75 → "1 hours 45 minutes"), and output only the result. '
        "Maximum 60 words per response."
    )
    user_prompt = data["message"]
    subject_context = []
    session_context = []
    for subject in Subjects.query.all(): #subject is an object
        subject_context.append(
            "\n\n"
            f"Subject: {subject.name}\n"
            f"Exam in: {(subject.exam_date - date.today()).days} day(s)\n"
            f"Progress: {subject.progress * 100}%\n"
            f"Priority score: {calculate_priority(subject)}\n"
            f"Difficulty: {subject.effective_difficulty}\n"
            f"Passion level: {subject.passion_level}\n"
            f"Importance: {subject.importance_weight}\n"
            "\n\n"
        )

    for session in STUDY_SESSIONS.query.filter_by(date = date.today()).order_by(STUDY_SESSIONS.subject_id):
        session_context.append(
            f"Study hours allocated for this subject: {session.allocated_hours} hour(s)\n"
            f"Subject completion status: {session.status}\n"
        )

    for i in range(len(subject_context)):
        user_prompt += subject_context[i] + "\n" + session_context[i]

    user_prompt += f"Total daily studying hours: {get_daily_hours()} hour(s)"
    result = call_llm(system_prompt, user_prompt)
    return jsonify({'response' : result})