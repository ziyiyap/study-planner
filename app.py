#Starts the server
from flask import Flask
from routes.ai import ai
from routes.dashboard import dashboard
from routes.planner import planner
from routes.progress import progress
from routes.subjects import subjects
import config 

app = Flask(__name__)

app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

app.register_blueprint(ai)
app.register_blueprint(dashboard)
app.register_blueprint(planner)
app.register_blueprint(progress)
app.register_blueprint(subjects)

if __name__ == "__main__":
    app.run(debug=True)