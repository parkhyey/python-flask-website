# Dependencies
from flask import Flask, render_template, request, redirect
import os
import database.db_connector as db
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

@app.route("/index")
def index():
    """Render index.html as home page"""
    return render_template("index.html")

@app.route("/index-user")
def index_user():
    return render_template("index-user.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/search-profiles")
def search():
    return render_template("search-profiles.html")

@app.route("/browse-profiles")
def browse():
    return render_template("browse-profiles.html")

@app.route("/daily-news")
def news():
    return render_template("daily-news.html")

@app.route("/create-profiles")
def create():
    return render_template("create-profiles.html")

@app.route("/manage-profiles", methods=["GET", "POST"])
def manage():
    db_connection = db.connect_to_database()
    # select all records from Instructors table joined with Campuses
    profiles_query = "SELECT * FROM Profiles;"
    profiles_cursor = db.execute_query(db_connection=db_connection, query=profiles_query)
    profiles_results = profiles_cursor.fetchall()

    db_connection.close()    
    return render_template("manage-profiles.html", items=profiles_results)

# Create profile
@app.route("/profiles", methods=["GET", "POST"])
def profile():
    db_connection = db.connect_to_database()

    if request.method == "POST":

        if request.form.get("Add_Profile"):
            profile_name = request.form["name"]
            profile_type = request.form["type"]
            profile_breed = request.form["breed"]
            profile_dispositions = request.form.getlist("disposition")
            profile_availability = request.form["availability"]
            profile_news = request.form["news"]
            profile_description = request.form["description"]

            # Join multiple entries for dispositions
            join_dispositions = ', '.join(profile_dispositions)

            profiles_query = "INSERT INTO Profiles (profile_name, profile_type, profile_breed, profile_disposition, profile_availability, profile_news, profile_description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur = db_connection.cursor()
            cur.execute(profiles_query, (profile_name, profile_type, profile_breed, join_dispositions, profile_availability, profile_news, profile_description))
            db_connection.commit()

        return redirect("/manage-profiles")

# Listener
if __name__ == "__main__":
    app.run(debug=True) # Use 'python app.py' or 'flask run' to run in terminal
