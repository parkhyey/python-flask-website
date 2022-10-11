# furever-friend-finder

## How to install Flask and run the app
```
$   py -3 -m venv .venv
$   .venv\scripts\activate
$   pip install Flask
$   pip install -r requirements.txt
$   python app.py
```
Helpful resource for Flask => https://github.com/osu-cs340-ecampus/flask-starter-app

## How to connect to the SQL database
Navigate to the root of your project on your local machine and create a file called .env. That's right, no name, just the extension. This will be a text file we keep our secrets in.

Inside that file, we write down our secrets in the following fashion:
```
DBHOST=sql3.freesqldatabase.com
DBUSER=sql3523753             
DBPW=J1EtV8wIeq
DB=sql3523753
```
