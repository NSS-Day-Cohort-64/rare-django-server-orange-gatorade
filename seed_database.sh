#!/bin/bash

rm db.sqlite3
rm -rf ./gatoradeapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations gatoradeapi
python3 manage.py migrate gatoradeapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata authors