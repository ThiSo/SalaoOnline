from flask import Flask, render_template
from flask_login import current_user
from main import app

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", user=current_user)