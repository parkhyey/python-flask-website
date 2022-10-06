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
![image](https://user-images.githubusercontent.com/71689421/194201871-d3f7d3b2-3a1a-4011-9f57-becca12708e8.png)
![image](https://user-images.githubusercontent.com/71689421/194202690-aa58f676-634f-4de6-93b6-34a78fb1b510.png)

## How to connect to the SQL database
Navigate to the root of your project on your local machine and create a file called .env. That's right, no name, just the extension. This will be a text file we keep our secrets in.

Inside that file, we write down our secrets in the following fashion:
```
DBHOST=sql3.freesqldatabase.com
DBUSER=sql3523753             
DBPW=J1EtV8wIeq
DB=sql3523753
```
![image](https://user-images.githubusercontent.com/71689421/194202582-879b35d0-18f7-4430-9a5a-8edc4053c65a.png)
