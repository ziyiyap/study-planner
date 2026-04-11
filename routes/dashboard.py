from flask import Blueprint, render_template

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/")
def dashb():
    return render_template("dashboard.html")