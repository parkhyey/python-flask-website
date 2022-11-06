# Dependencies
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import database.db_connector as db
import datetime
from dateutil.relativedelta import relativedelta
from flask_mail import Mail, Message
import smtplib
from threading import Thread

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

# Email Configuration (testing server)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'fureverfriendfinder1@gmail.com'
app.config['MAIL_PASSWORD'] = 'tfeuljljvwrxttxi'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
SENDER = 'admin@fureverfriendfinder.com'

# Routes
# Home
@app.route("/")
def root():
    db_connection = db.connect_to_database()
    cur = db_connection.cursor()
    news_query= """SELECT n.*, p.profile_image
        FROM News n
        JOIN Profiles p ON n.profile_id = p.profile_id
        ORDER BY news_date DESC"""
    cursor = db.execute_query(db_connection, news_query)
    animal_news = cursor.fetchall()
    db_connection.close()
    """Render index.html as home page"""
    return render_template("index.html", stories=animal_news)

@app.route("/index")
def index():
    """Render index.html as home page"""
    return redirect(url_for('root'))

@app.route("/index-user")
def index_user():
    return render_template("index-user.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/user-profile")
def user_profile():
    db_connection = db.connect_to_database()
    id = session["id"]
    # query to grab the info and display on modal
    modal_query = "SELECT * FROM Users WHERE user_id = %s"

    cur = db_connection.cursor()
    cur.execute(modal_query, (id,))
    data = cur.fetchone()

    return render_template("user-profile.html", data=data)

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
                session["id"] = account_result[0]
                session["fname"] = account_result[1]
                session["lname"] = account_result[2]
                session["email"] = account_result[3]
                session["password"] = account_result[4]
                session["is_admin"] = account_result[5]
                db_connection.close()
                return redirect("/")
            else:
                flash("Incorrect username/password! Please try again.", 'error')
                db_connection.close()
                return redirect("/login")

    return render_template("login.html")


@app.route("/edit-user/<int:id>", methods=["GET", "POST"])
def edit_user(id):

    if request.method == "POST":
        db_connection = db.connect_to_database()

        # Grab user form inputs
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]

        # User toggles switch to 'Change Password'
        if request.form.get('toggleSwitch'):

            password = request.form["password"]
            password_confirmation = request.form["confirmation"]

            # Error handling for password and confirmation password
            if(password == password_confirmation):
                update_user_query = "UPDATE Users SET user_fname = %s, user_lname = %s, user_email = %s, user_password = SHA1(%s) WHERE user_id = %s;"
                cur = db_connection.cursor()
                cur.execute(update_user_query, (fname, lname, email, password, id))
                db_connection.commit()
                db_connection.close()
                flash("Profile updated!", 'success')
                return redirect("/user-profile")
            else:
                flash("Passwords do not match! Please try again.", 'error')
                return redirect("/user-profile")
        else:
            update_user_query = "UPDATE Users SET user_fname = %s, user_lname = %s, user_email = %s WHERE user_id = %s;"
            cur = db_connection.cursor()
            cur.execute(update_user_query, (fname, lname, email, id))
            db_connection.commit()
            db_connection.close()
            flash("Profile updated!", 'success')
            return redirect("/user-profile")

@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    session.clear()
    return redirect("/")

@app.route("/search-profiles", methods=["GET", "POST"])
def search():
    db_connection = db.connect_to_database()
    cur = db_connection.cursor()

    disp_qry = "SELECT disposition_value FROM Dispositions"
    cur.execute(disp_qry)
    disp_results = cur.fetchall()

    animal_qry = "SELECT * FROM Animals"
    cur.execute(animal_qry)
    animals_results = cur.fetchall()

    disp_qry = "SELECT * FROM Dispositions"
    disp_cursor = db.execute_query(db_connection=db_connection, query=disp_qry)
    disp = disp_cursor.fetchall()

    drop_temp_qry = "DROP TABLE IF EXISTS Temp;"
    drop_temp_cursor = db.execute_query(db_connection=db_connection, query=drop_temp_qry)
    drop_temp_results = drop_temp_cursor.fetchall()

    create_temp_qry = "CREATE TABLE Temp AS SELECT p.profile_id as profile_id, profile_name, profile_type, profile_breed, GROUP_CONCAT(d.disposition_value) AS disp, profile_availability, profile_description, profile_image, profile_created_at \
        FROM Profiles p \
        JOIN Profiles_Dispositions pd ON p.profile_id = pd.profile_id \
        JOIN Dispositions d ON pd.disposition_id = d.disposition_id \
        GROUP BY p.profile_id \
        ORDER BY p.profile_id ASC;"
    create_temp_cursor = db.execute_query(db_connection=db_connection, query=create_temp_qry)
    create_temp_results = create_temp_cursor.fetchall()

    select_qry = "SELECT * FROM Temp;"
    select_cursor = db.execute_query(db_connection=db_connection, query=select_qry)
    select_results = select_cursor.fetchall()

    # display all results before search
    search_results = select_results

    # search data when form is submitted
    if request.method == "POST":
        profile_type = request.form.get('type')
        profile_breed = request.form.get('breed')
        disposition_value = request.form.get('disposition')
        if disposition_value != "Any":
            disposition_value = "%"+ request.form.get('disposition') + "%"
        profile_created_at = request.form.get('created')

        # set dates per search option
        start_date = '1900-01-01 00:00:00'
        current_date = datetime.datetime.today()
        if profile_created_at == "Past 24 hours":
            start_date = current_date - relativedelta(hours=24) 
        elif profile_created_at == "Past Week":
            start_date = current_date - relativedelta(days=7) 
        elif profile_created_at == "Past Month":
            start_date = current_date - relativedelta(months=1)
        elif profile_created_at == "Past Year":
            start_date = current_date - relativedelta(years=1)
        # print(profile_created_at, "/ current_date=", current_date, "/ start_date=", start_date)

        if profile_type == "Any" and disposition_value == "Any":
            search_qry = "SELECT * from Temp \
                WHERE profile_created_at BETWEEN %s AND %s \
                GROUP BY profile_id \
                ORDER BY profile_id ASC;"
            data_params = (start_date, current_date)        
            search_cursor = db.execute_query(db_connection=db_connection, query=search_qry, query_params=data_params)
            search_results = search_cursor.fetchall()

        elif profile_type == "Any" and disposition_value != "Any":
            search_qry = "SELECT * from Temp \
                WHERE disp LIKE %s AND profile_created_at BETWEEN %s AND %s \
                GROUP BY profile_id \
                ORDER BY profile_id ASC;"
            data_params = (disposition_value, start_date, current_date)        
            search_cursor = db.execute_query(db_connection=db_connection, query=search_qry, query_params=data_params)
            search_results = search_cursor.fetchall()

        elif profile_type!= "Any" and profile_breed == "Any" and disposition_value == "Any":
            search_qry = "SELECT * from Temp \
                WHERE profile_type = %s AND profile_created_at BETWEEN %s AND %s \
                GROUP BY profile_id \
                ORDER BY profile_id ASC;"
            data_params = (profile_type, start_date, current_date)        
            search_cursor = db.execute_query(db_connection=db_connection, query=search_qry, query_params=data_params)
            search_results = search_cursor.fetchall()

        elif profile_type!= "Any" and profile_breed == "Any" and disposition_value != "Any":
            search_qry = "SELECT * from Temp \
                WHERE profile_type = %s AND disp LIKE %s AND profile_created_at BETWEEN %s AND %s \
                GROUP BY profile_id \
                ORDER BY profile_id ASC;"
            data_params = (profile_type, disposition_value, start_date, current_date)        
            search_cursor = db.execute_query(db_connection=db_connection, query=search_qry, query_params=data_params)
            search_results = search_cursor.fetchall()

        elif profile_type!= "Any" and profile_breed != "Any" and disposition_value == "Any":
            search_qry = "SELECT * from Temp \
                WHERE profile_type = %s AND profile_breed = %s AND profile_created_at BETWEEN %s AND %s \
                GROUP BY profile_id \
                ORDER BY profile_id ASC;"
            data_params = (profile_type, profile_breed, start_date, current_date)        
            search_cursor = db.execute_query(db_connection=db_connection, query=search_qry, query_params=data_params)
            search_results = search_cursor.fetchall()

        else:
            search_qry = "SELECT * from Temp \
                WHERE profile_type = %s AND profile_breed = %s AND disp LIKE %s AND profile_created_at BETWEEN %s AND %s \
                GROUP BY profile_id \
                ORDER BY profile_id ASC;"
            data_params = (profile_type, profile_breed, disposition_value, start_date, current_date)        
            search_cursor = db.execute_query(db_connection=db_connection, query=search_qry, query_params=data_params)
            search_results = search_cursor.fetchall()
        
        # if no search result, display error message
        if len(search_results) == 0 or search_results[0].get("profile_id") == None: 
            flash("No Results Found.", 'error')
            search_results = ""

    data = {
        "profile": select_results,
        "dispositions": disp_results,
        "animals": animals_results,
        "search" : search_results,
        "disp" : disp
    }
    db_connection.close()    
    return render_template("search-profiles.html", data=data)

@app.route("/check-session/<page>/<int:id>", methods=["GET", "POST"])
def check_session(page, id):
    """Check if user session exists"""
    if session.get('logged_in') == True:
        user_email = session.get('email')
        return redirect(url_for("date_request", page=page, id = id, user_email = user_email))
    else:
        return redirect(url_for("login"))

@app.route("/date-request/<page>/<int:id>/<user_email>", methods=["GET"])
def date_request(page, id, user_email):
    """Get a date request, update profile availbility, add Date_Requests data and send confirmation email to user"""
    db_connection = db.connect_to_database()
    if request.method == "GET":
        available = "Available"
        pending = "Pending"
        
        # verify profile_availability
        select_qry = "SELECT * FROM Profiles \
            WHERE profile_id = %s AND profile_availability = %s;"
        data_params = (id, available)
        select_cursor = db.execute_query(db_connection=db_connection, query=select_qry, query_params=data_params)
        select_results = select_cursor.fetchall()   

        # update profile_availability
        request_qry = "UPDATE Profiles \
            SET profile_availability = %s \
            WHERE profile_id = %s;"
        data_params_req = (pending, id)
        request_cursor = db.execute_query(db_connection=db_connection, query=request_qry, query_params=data_params_req)
        request_results = request_cursor.fetchall()

        # add Date_Requests data
        insert_qry = "INSERT INTO Date_Requests (profile_id, user_email) VALUES (%s, %s);"
        data_params_insert = (id, user_email)
        insert_cursor = db.execute_query(db_connection=db_connection, query=insert_qry, query_params=data_params_insert)
        insert_results = request_cursor.fetchall()

    if len(select_results) == 0:
        flash("To request a date, the animal profile must be available.", 'error')

    elif len(select_results) > 0:
        flash("You have successfully requested a date! Check your email for confirmation.", 'success')
        if user_email:
            message = Message(
                sender = SENDER, 
                subject="Your Date Request Confirmation",
                recipients=[user_email],
                html = render_template('email/date-notification.html'),
                )
            mail.send(message)

    db_connection.close()    
    return redirect(url_for(page))

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
        check_query = "SELECT * FROM Date_Requests WHERE profile_id = %s;"
        check_cursor = db.execute_query(db_connection=db_connection, query=check_query, query_params=data)
        check_results = check_cursor.fetchall()
        if len(check_results) > 0:
            delete_date_query = "DELETE FROM Date_Requests WHERE profile_id = %s"
            delete_date_cursor = db.execute_query(db_connection=db_connection, query=delete_date_query, query_params=data)
            delete_date_results = delete_date_cursor.fetchall()            
        # get image file name
        profile_img = select_results[0].get('profile_image')
        delete_profiles_disposition_query = "DELETE FROM Profiles_Dispositions WHERE profile_id = %s;"
        delete_news_query = "DELETE FROM News WHERE profile_id = %s"
        delete_profiles_query = "DELETE FROM Profiles WHERE profile_id = %s AND profile_availability = 'Not available';"
        delete_profiles_disposition_cursor = db.execute_query(db_connection=db_connection, query=delete_profiles_disposition_query, query_params=data)
        delete_news_cursor = db.execute_query(db_connection, delete_news_query, data)
        delete_profiles_cursor = db.execute_query(db_connection=db_connection, query=delete_profiles_query, query_params=data)
        # flash success messages
        flash("You have deleted profile id #" + str(id) + ".", 'success')

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

            # Insert into News table
            news_query = "INSERT INTO News (profile_id, news_description) VALUES (@profile_id, %s);"
            cur = db_connection.cursor()
            cur.execute(news_query, (_profile['news'],))

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
                if _profile["availability"] == "Available":
                    # Send notification email
                    notification_send()
                    flash("Your profile has been created! A notification email has been sent to all users.", 'success')
                else:
                    flash("Your profile has been created!", 'success')
                db_connection.close()
                return redirect("/manage-profiles")

def send_email_thread(message):
    with app.app_context():
        mail.send(message)

def notification_send():
    db_connection = db.connect_to_database()
    select_user_qry = "SELECT DISTINCT user_email FROM Users;"
    cur = db_connection.cursor()
    cur.execute(select_user_qry)
    users = cur.fetchall()

    new_profile_qry = "SELECT profile_name, profile_type, profile_breed, profile_description, profile_image FROM Profiles ORDER BY profile_id DESC LIMIT 1;"
    cur = db_connection.cursor()
    cur.execute(new_profile_qry)
    new_profile = cur.fetchone()
    print("new_profile", new_profile)
    html = render_template('email/new-notification.html', item = new_profile)

    with app.app_context():
        for i in range(len(users)):
            message = Message(
                sender = SENDER, 
                subject="Meet our new furry friends!",
                recipients=[users[i][0]],
                html = html
                )
            print("email(", i, ")=", users[i][0])
            Thread(target=send_email_thread, args=[message]).start()
    db_connection.close()

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
            curr_news = curr_profile[5]

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

            # News - only add to News table if news has changed
            if _profile["news"] != curr_news:
                news_query = "INSERT INTO News (profile_id, news_description) VALUES (%s, %s);"
                cur = db_connection.cursor()
                cur.execute(news_query, (int(id), _profile['news']))


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
