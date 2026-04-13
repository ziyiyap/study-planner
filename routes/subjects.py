from flask import Blueprint, render_template, request, redirect, url_for
from datetime import date, datetime
from models.database import db,Subjects, PDF_DOCUMENTS
from datetime import date, datetime
from services.pdf_service import process_pdf
from services.ai_service import analyze_difficulty, summarize_pdf
from services.scoring_service import calculate_effective_difficulty
from werkzeug.utils import secure_filename
import os
import config


subjects_bp = Blueprint('subjects', __name__)

@subjects_bp.route("/subjects", methods = ["GET"])
def query():
    all_subjects = Subjects.query.order_by(Subjects.exam_date).all()
    return render_template("subjects.html", today=date.today(),subjects = all_subjects)

@subjects_bp.route("/subjects/add", methods = ["POST"])
def call():
    name = request.form.get('name')
    exam_date = request.form.get('exam_date')
    passion_level = request.form.get('passion_level')
    importance_weight = (float(request.form.get('importance_weight')) / 10) * 3

    file = request.files.get("pdf")

    if file and file.filename != "":
        filename = secure_filename(file.filename)

        file_path = config.UPLOAD_FOLDER / filename
        file.save(file_path)

        pdf_info = process_pdf(file_path)
        summary = summarize_pdf(pdf_info['chunks'])
        objective_difficulty = analyze_difficulty(summary, pdf_info["doc_type"])
        
        pdf_object = PDF_DOCUMENTS(
            filename = filename,
            uploaded_at = datetime.now(),
            cleaned_text = pdf_info["cleaned_text"],
            summary = summary,
            objective_difficulty = objective_difficulty
        )

        db.session.add(pdf_object)
        db.session.commit()

        pdf_id = pdf_object.id
   
    else:
        pdf_id = None
        objective_difficulty = float(request.form.get("objective_difficulty")) / 10

    effective_difficulty = calculate_effective_difficulty(objective_difficulty, passion_level)
    subject_object = Subjects(
        pdf_id = pdf_id,
        name = name,
        exam_date = datetime.strptime(exam_date, "%Y-%m-%d").date(),
        objective_difficulty = objective_difficulty,
        passion_level = float(passion_level),
        effective_difficulty = effective_difficulty,
        importance_weight = float(importance_weight),
        created_at = datetime.now()
    )

    db.session.add(subject_object)
    db.session.commit()

    return redirect(url_for('subjects.query'))

@subjects_bp.route("/subjects/delete", methods = ["POST"])
def delete():
    subject_id = request.form.get("subject_id")
    result = Subjects.query.get(subject_id)
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('subjects.query'))

@subjects_bp.route("/subjects/update", methods = ["POST"])
def update():
    subject_id = request.form.get("subject_id")
    progress = request.form.get("progress")
    subject = Subjects.query.get(subject_id)
    subject.progress = float(progress)
    db.session.commit()
    return redirect(url_for('subjects.query'))