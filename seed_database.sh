#!/bin/bash

rm db.sqlite3
rm -rf ./newsapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations newsapi
python3 manage.py migrate newsapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

