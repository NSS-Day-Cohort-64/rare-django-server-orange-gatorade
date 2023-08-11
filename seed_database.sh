#!/bin/bash

rm db.sqlite3
rm -rf ./gatoradeapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations gatoradeapi
python3 manage.py migrate gatoradeapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata authors
python3 manage.py loaddata categories
python3 manage.py loaddata tags
python3 manage.py loaddata reactions
python3 manage.py loaddata posts
python3 manage.py loaddata post_tags
python3 manage.py loaddata post_reactions