# furever-friend-finder

## How to install Flask and run the app
```
$   py -3 -m venv .venv
$   .venv\scripts\activate
$   pip install Flask
$   pip install -r requirements.txt
$   python app.py
```
Please note there are some unnecessary dependencies in requirements.txt which I will clean-up later.
This repo is helpful to understand flask => https://github.com/osu-cs340-ecampus/flask-starter-app

Currently it's obviously super basic. I wanted to setup a base flask app to start with. Please feel free to add/edit/delete anythings.
![image](https://user-images.githubusercontent.com/71689421/194203921-fb4d7ad2-1880-48da-9d14-31162572fad9.png)
![image](https://user-images.githubusercontent.com/71689421/194203977-55b49fb0-2936-409d-9612-9de239116027.png)

## How to connect to the SQL database
Navigate to the root of your project on your local machine and create a file called .env. That's right, no name, just the extension. This will be a text file we keep our secrets in.

Inside that file, we write down our secrets in the following fashion:
```
DBHOST=sql3.freesqldatabase.com
DBUSER=sql3523753             
DBPW=J1EtV8wIeq
DB=sql3523753
```
![image](https://user-images.githubusercontent.com/71689421/194204003-af4b3135-2e3d-425c-9876-2bab7e2f1b76.png)
