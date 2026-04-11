from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class PDF_DOCUMENTS(db.Model):
    __tablename__ = "pdf_docs"

    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime)
    cleaned_text = db.Column(db.Text)
    summary = db.Column(db.Text)
    objective_difficulty = db.Column(db.Float)

    subject = db.relationship("Subjects", backref = "pdf")

class Subjects(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key = True)
    pdf_id = db.Column(db.Integer, db.ForeignKey('pdf_docs.id'))
    name = db.Column(db.String(100))
    exam_date = db.Column(db.Date)
    objective_difficulty = db.Column(db.Float)
    passion_level = db.Column(db.Float)
    effective_difficulty = db.Column(db.Float)
    importance_weight = db.Column(db.Float)
    progress = db.Column(db.Float, default = 0.0)
    created_at = db.Column(db.DateTime)

    ai_insight = db.relationship("AIInsight", backref = "subj")
    study_session = db.relationship("STUDY_SESSIONS", backref = 'subj')

class AIInsight(db.Model):
    __tablename__ = "ai_insights"

    id = db.Column(db.Integer, primary_key = True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    insight_text = db.Column(db.Text)
    generated_at = db.Column(db.DateTime)
    is_read = db.Column(db.Boolean, default = False)

class STUDY_SESSIONS(db.Model):
    __tablename__ = "study_sessions"

    id = db.Column(db.Integer, primary_key = True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    date = db.Column(db.Date)
    allocated_hours = db.Column(db.Float)
    actual_hours = db.Column(db.Float, default = 0.0)
    status = db.Column(db.String(20), default = 'pending')

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()