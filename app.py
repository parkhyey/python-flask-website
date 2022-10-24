# Dependencies
from flask import Flask, render_template, request, redirect, url_for, flash, session
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

@app.route("/user-profile")
def user_profile():

    return render_template("user-profile.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    db_connection = db.connect_to_database()

    if request.method == "POST":

        if request.form.get("Register_User"):
            user_fname = request.form["fname"]
            user_lname = request.form["lname"]
            user_email = request.form["email"]
            user_password = request.form["password"]
            user_password_confirmation = request.form["confirmation"]
            user_is_admin = request.form["admin"]

            # Select Users table for account verifcation
            users_select_query = "SELECT * FROM Users WHERE user_email = %s"

            cur = db_connection.cursor()
            cur.execute(users_select_query, (user_email, ))

            account = cur.fetchone()

            if account:
                flash("Account already exists!", 'error')
                return redirect("/signup")
            elif user_password_confirmation == user_password:
                # Insert into Users table
                users_insert_query = "INSERT INTO Users (user_fname, user_lname, user_email, user_password, user_is_admin) VALUES (%s, %s, %s, SHA1(%s), %s);"

                cur.execute(users_insert_query, (user_fname, user_lname, user_email, user_password, user_is_admin))

                db_connection.commit()
                flash("Your account has been created! Please sign in", 'success')
                db_connection.close()
                return redirect("/login")
            else:
                flash("Passwords do not match! Please try again.", 'error')
                return redirect("/signup")

@app.route("/login", methods=["GET", "POST"])
def login():
    db_connection = db.connect_to_database()

    if request.method == "POST":

        if request.form.get("User_Login"):
            user_email = request.form["email"]
            user_password = request.form["password"]

            login_query = "SELECT * FROM Users WHERE user_email = %s AND user_password = SHA1(%s)"

            cur = db_connection.cursor()
            cur.execute(login_query, (user_email, user_password))

            account_result = cur.fetchone()

            if account_result:
                session["logged_in"] = True
                session["fname"] = account_result[1]
                session["lname"] = account_result[2]
                session["email"] = account_result[3]
                session["password"] = account_result[4]
                session["is_admin"] = account_result[5]
                db_connection.close()
                return render_template("index.html", account = account_result)
            else:
                flash("Incorrect username/password! Please try again.", 'error')
                db_connection.close()
                return redirect("/login")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    return render_template("index.html")

@app.route("/search-profiles")
def search():
    return render_template("search-profiles.html")

@app.route("/browse-profiles")
def browse():
    db_connection = db.connect_to_database()
    cur = db_connection.cursor()
    profiles_query = """SELECT Profiles.profile_id, Profiles.profile_name, 
        Profiles.profile_type, Profiles.profile_breed, 
        GROUP_CONCAT(Dispositions.disposition_value), 
        Profiles.profile_availability, Profiles.profile_news, 
        Profiles.profile_description, Profiles.profile_image 
        FROM Profiles_Dispositions 
        JOIN Profiles ON Profiles_Dispositions.profile_id = Profiles.profile_id 
        JOIN Dispositions ON Profiles_Dispositions.disposition_id = Dispositions.disposition_id 
        GROUP BY Profiles.profile_id;"""
    cursor = db.execute_query(db_connection, profiles_query)
    profiles = cursor.fetchall()

    db_connection.close()
    return render_template("browse-profiles.html", items=profiles, len=len(profiles))

@app.route("/daily-news")
def news():
    return render_template("daily-news.html")

@app.route("/create-profiles")
def create():
    db_connection = db.connect_to_database()
    cur = db_connection.cursor()

    disp_qry = "SELECT * FROM Dispositions"
    cur.execute(disp_qry)
    disp = cur.fetchall()

    animal_qry = "SELECT * FROM Animals"
    cur.execute(animal_qry)
    animals = cur.fetchall()

    data = {
        "dispositions": disp,
        "animals": animals
    }

    db_connection.close()
    return render_template("create-profiles.html", data=data)

@app.route("/manage-profiles", methods=["GET"])
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


def get_profile_form_values(request):
    return {
        "name": request.form["name"],
        "type": request.form["type"],
        "breed": request.form["breed"],
        "dispositions": {
            "1": request.form.getlist("disposition1"),
            "2": request.form.getlist("disposition2"),
            "3": request.form.getlist("disposition3"),
        },
        "availability": request.form["availability"],
        "news": request.form["news"],
        "description": request.form["description"],
        "picture": request.files.get("picture", None)
    }


# Create profile
@app.route("/profiles", methods=["GET", "POST"])
def profile():
    db_connection = db.connect_to_database()

    if request.method == "POST":

        if request.form.get("Add_Profile"):
            _profile = get_profile_form_values(request)

            # Save uploaded picture
            filename = _profile["picture"].filename
            _profile["picture"].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Insert into Profiles table
            profiles_query = "INSERT INTO Profiles (profile_name, profile_type, profile_breed, profile_availability, profile_news, profile_description, profile_image) VALUES (%s, %s, %s, %s, %s, %s, %s); SET @profile_id = LAST_INSERT_ID()"
            cur = db_connection.cursor()
            cur.execute(profiles_query, (_profile["name"], _profile["type"], _profile["breed"], _profile["availability"], _profile["news"], _profile["description"], filename))

            # Insert into Profiles_Dispositions table
            disposition_query = "INSERT INTO Profiles_Dispositions (profile_id, disposition_id) VALUES (@profile_id, %s);"
            cur = db_connection.cursor()

            if _profile["dispositions"]["1"]:
                cur.execute(disposition_query, _profile["dispositions"]["1"])
            if _profile["dispositions"]["2"]:
                cur.execute(disposition_query, _profile["dispositions"]["2"])
            if _profile["dispositions"]["3"]:
                cur.execute(disposition_query, _profile["dispositions"]["3"])

            # At least one disposition is not selected
            if len(_profile["dispositions"]["1"]) == 0 and len(_profile["dispositions"]["2"]) == 0 and len(_profile["dispositions"]["3"]) == 0:
                flash("Please select at least one disposition", 'error')
                return redirect("/create-profiles")
            else: 
                db_connection.commit()
                # Success message
                flash("Your profile has been created!", 'success')
                db_connection.close()
                return redirect("/manage-profiles")


@app.route('/profiles/<int:id>', methods=["GET", "PUT"])
def profile_id(id):
    if request.method == "GET":
        db_connection = db.connect_to_database()
        cur = db_connection.cursor()

        curr_profile_qry = "SELECT * FROM Profiles WHERE profile_id = %s"
        cur.execute(curr_profile_qry, (int(id),))
        curr_profile = cur.fetchone()

        profile_disp_qry = """SELECT d.* 
            FROM Dispositions d
            JOIN Profiles_Dispositions pd ON d.disposition_id = pd.disposition_id
            JOIN Profiles p ON p.profile_id = pd.profile_id
            WHERE p.profile_id = %s"""
        cur.execute(profile_disp_qry, (int(id),))
        profile_disp = cur.fetchall()

        disp_qry = "SELECT * FROM Dispositions"
        cur.execute(disp_qry)
        disp = cur.fetchall()

        animal_qry = "SELECT * FROM Animals"
        cur.execute(animal_qry)
        animals = cur.fetchall()

        data = {
            "profile": curr_profile,
            "profile_dispositions": profile_disp,
            "dispositions": disp,
            "animals": animals
        }
        db_connection.close()
        return render_template("create-profiles.html", data=data)
    elif request.method == "PUT":
        db_connection = db.connect_to_database()
        cur = db_connection.cursor()

        if request.form.get("name"):
            _profile = get_profile_form_values(request)

            # At least one disposition is not selected
            if len(_profile["dispositions"]["1"]) == 0 and len(
                    _profile["dispositions"]["2"]) == 0 and len(
                    _profile["dispositions"]["3"]) == 0:
                flash("Please select at least one disposition", 'error')
                return redirect("/profiles/" + id)

            # Get existing profile
            curr_profile_qry = "SELECT * FROM Profiles WHERE profile_id = %s"
            cur.execute(curr_profile_qry, (int(id),))
            curr_profile = cur.fetchone()
            curr_img = curr_profile[7]

            filename = "";
            if len(_profile["picture"].filename) > 0:
                filename = _profile["picture"].filename
                # if picture is being changed
                if curr_img != filename:
                    # save the new image
                    _profile["picture"].save(os.path.join(UPLOAD_FOLDER, filename))
                    # delete the old image if it exists and is not a sample image
                    if curr_img not in SAMPLE_IMAGES and os.path.exists(
                            os.path.join(UPLOAD_FOLDER, curr_img)):
                        os.remove(os.path.join(UPLOAD_FOLDER, curr_img))
            else:
                filename = curr_img

            # delete dispositions and resave them to update
            disp_delete_qry = "DELETE FROM Profiles_Dispositions WHERE profile_id = %s"
            cur.execute(disp_delete_qry, (int(id),))

            # add dispositions
            disp_add_qry = "INSERT INTO Profiles_Dispositions (profile_id, disposition_id) VALUES (%s, %s)"
            if _profile["dispositions"]["1"]:
                cur.execute(disp_add_qry, (id, _profile["dispositions"]["1"]))
            if _profile["dispositions"]["2"]:
                cur.execute(disp_add_qry, (id, _profile["dispositions"]["2"]))
            if _profile["dispositions"]["3"]:
                cur.execute(disp_add_qry, (id, _profile["dispositions"]["3"]))

            # update profile
            profile_qry = """UPDATE Profiles SET profile_name = %s, 
                profile_type = %s, profile_breed = %s, profile_availability=%s,
                profile_news=%s, profile_description=%s, profile_image=%s 
                WHERE profile_id=%s"""
            if _profile["picture"] is None:
                _profile["picture"] = curr_img
            cur.execute(profile_qry, (_profile["name"], _profile["type"],
                                      _profile["breed"],
                                      _profile["availability"],
                                      _profile["news"],
                                      _profile["description"], filename,
                                      int(id)))

            db_connection.commit()

            flash("Your profile has been updated!", 'success')
            db_connection.close()
            return { "Result": "Success" }, 200


# Listener
if __name__ == "__main__":
    app.run(debug=True) # Use 'python app.py' or 'flask run' to run in terminal
