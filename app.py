#Starts the server
from flask import Flask
from routes.ai import ai
from routes.dashboard import dashboard
from routes.planner import planner
from routes.progress import progress
from routes.subjects import subjects_bp
from routes.calendar import calendar
from routes.settings import settings
import config 
from models.database import init_db
import os

os.chdir(config.BASE_DIR)


app = Flask(__name__)

app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(config.DATABASE_PATH)
app.register_blueprint(ai)
app.register_blueprint(dashboard)
app.register_blueprint(planner)
app.register_blueprint(progress)
app.register_blueprint(subjects_bp)
app.register_blueprint(calendar)
app.register_blueprint(settings)

init_db(app)

if __name__ == "__main__":
    app.run(debug=True)