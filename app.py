# Dependencies
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import database.db_connector as db
import datetime

# Define Upload folder
UPLOAD_FOLDER = "static/img/profile"
ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])

# Sample images
SAMPLE_IMAGES = ['goat.jpg', 'golden.jpg', 'gsd.jpg', 'hamster.jpg', 'persian.jpg', 'pom.jpg', 'poodle.jpg', 'siamese.jpg']

# Configuration
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "secret"  

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
    profiles_query = "SELECT Profiles.profile_id, Profiles.profile_name, Profiles.profile_type, Profiles.profile_breed, GROUP_CONCAT(Dispositions.disposition_value), Profiles.profile_availability, Profiles.profile_news, Profiles.profile_description, Profiles.profile_image FROM Profiles_Dispositions JOIN Profiles ON Profiles_Dispositions.profile_id = Profiles.profile_id JOIN Dispositions ON Profiles_Dispositions.disposition_id = Dispositions.disposition_id GROUP BY Profiles.profile_id;"
    profiles_cursor = db.execute_query(db_connection=db_connection, query=profiles_query)
    profiles_results = profiles_cursor.fetchall()

    db_connection.close()    
    return render_template("manage-profiles.html", items=profiles_results)

@app.route("/delete-profiles/<int:id>")
def delete_profiles(id):
    """Delete an animal profile from the Profiles table"""
    db_connection = db.connect_to_database()
    data = (id,)
    select_query = "SELECT * FROM Profiles WHERE profile_id = %s AND profile_availability = 'Not available';"
    select_cursor = db.execute_query(db_connection=db_connection, query=select_query, query_params=data)
    select_results = select_cursor.fetchall()
    profile_img = ""
    # verify if result exists
    if len(select_results) == 0:
        # flash error messages
        flash("To delete a profile, the profile availability must be 'Not available'.", 'error')
    else:
        # get image file name
        profile_img = select_results[0].get('profile_image')
        delete_profiles_disposition_query = "DELETE FROM Profiles_Dispositions WHERE profile_id = %s;"
        delete_profiles_query = "DELETE FROM Profiles WHERE profile_id = %s AND profile_availability = 'Not available';"
        delete_profiles_disposition_cursor = db.execute_query(db_connection=db_connection, query=delete_profiles_disposition_query, query_params=data)
        delete_profiles_cursor = db.execute_query(db_connection=db_connection, query=delete_profiles_query, query_params=data)
        # flash success messages
        flash("You have deleted profile id #" + str(id) + ".")

    # delete the select image file if exists
    if profile_img and os.path.exists(UPLOAD_FOLDER+"/"+profile_img):
        # ignore the sample images
        if not profile_img in SAMPLE_IMAGES:
            os.remove(UPLOAD_FOLDER+"/"+profile_img)

    db_connection.close()
    return redirect(url_for('manage'))

# Create profile
@app.route("/profiles", methods=["GET", "POST"])
def profile():
    db_connection = db.connect_to_database()

    if request.method == "POST":

        if request.form.get("Add_Profile"):
            profile_name = request.form["name"]
            profile_type = request.form["type"]
            profile_breed = request.form["breed"]
            profile_disposition1 = request.form.getlist("disposition1")
            profile_disposition2 = request.form.getlist("disposition2")
            profile_disposition3 = request.form.getlist("disposition3")
            profile_availability = request.form["availability"]
            profile_news = request.form["news"]
            profile_description = request.form["description"]
            picture = request.files["picture"]

            # Save uploaded picture
            filename = picture.filename
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Insert into Profiles table
            profiles_query = "INSERT INTO Profiles (profile_name, profile_type, profile_breed, profile_availability, profile_news, profile_description, profile_image) VALUES (%s, %s, %s, %s, %s, %s, %s); SET @profile_id = LAST_INSERT_ID()"
            cur = db_connection.cursor()
            cur.execute(profiles_query, (profile_name, profile_type, profile_breed, profile_availability, profile_news, profile_description, filename))

            # Insert into Profiles_Dispositions table
            disposition_query = "INSERT INTO Profiles_Dispositions (profile_id, disposition_id) VALUES (@profile_id, %s);"
            cur = db_connection.cursor()

            if profile_disposition1:
                cur.execute(disposition_query, profile_disposition1)
            if profile_disposition2:
                cur.execute(disposition_query, profile_disposition2)
            if profile_disposition3:
                cur.execute(disposition_query, profile_disposition3)

            # At least one disposition is not selected
            if len(profile_disposition1) == 0 and len(profile_disposition2) == 0 and len(profile_disposition3) == 0:
                flash("Please select at least one disposition", 'error')
                return redirect("/create-profiles")
            else: 
                db_connection.commit()
                # Success message
                flash("Your profile has been created!", 'success')
                db_connection.close()
                return redirect("/manage-profiles")

# Listener
if __name__ == "__main__":
    app.run(debug=True) # Use 'python app.py' or 'flask run' to run in terminal
