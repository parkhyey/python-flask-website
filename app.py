# Dependencies
from flask import Flask, render_template
import os
import datetime

# Configuration
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)

# Routes
# Home
@app.route("/")
def root():
    """Render index.html as home page"""
    return render_template("index.html")

@app.route("/index.html")
def index():
    """Render index.html as home page"""
    return render_template("index.html")

@app.route("/index-user.html")
def index_user():
    return render_template("index-user.html")

@app.route("/signup.html")
def signup():
    return render_template("signup.html")

@app.route("/login.html")
def login():
    return render_template("login.html")

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7676))
    app.run(port=port, debug=True) # Use 'python app.py' or 'flask run' to run in terminal
