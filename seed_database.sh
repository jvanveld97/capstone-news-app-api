#!/bin/bash

rm db.sqlite3
rm -rf ./newsapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations newsapi
python3 manage.py migrate newsapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata usersavedarticle
python3 manage.py loaddata moods
python3 manage.py loaddata comments
python manage.py loaddata topics


