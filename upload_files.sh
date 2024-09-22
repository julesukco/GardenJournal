#!/bin/bash
scp -i ~/.ssh/LightsailDefaultKey-us-west-2.pem '/Users/julianbishop/Library/Mobile Documents/com~apple~CloudDocs/Projects/GardenJournal/app.py' ubuntu@44.235.31.125:/home/ubuntu/flask_app/
scp -i ~/.ssh/LightsailDefaultKey-us-west-2.pem '/Users/julianbishop/Library/Mobile Documents/com~apple~CloudDocs/Projects/GardenJournal/requirements.txt' ubuntu@44.235.31.125:/home/ubuntu/flask_app/
scp -i ~/.ssh/LightsailDefaultKey-us-west-2.pem '/Users/julianbishop/Library/Mobile Documents/com~apple~CloudDocs/Projects/GardenJournal/query_db.py' ubuntu@44.235.31.125:/home/ubuntu/flask_app/
scp -i ~/.ssh/LightsailDefaultKey-us-west-2.pem '/Users/julianbishop/Library/Mobile Documents/com~apple~CloudDocs/Projects/GardenJournal/Read.me' ubuntu@44.235.31.125:/home/ubuntu/flask_app/
scp -i ~/.ssh/LightsailDefaultKey-us-west-2.pem '/Users/julianbishop/Library/Mobile Documents/com~apple~CloudDocs/Projects/GardenJournal/restart.sh' ubuntu@44.235.31.125:/home/ubuntu/flask_app/
scp -i ~/.ssh/LightsailDefaultKey-us-west-2.pem '/Users/julianbishop/Library/Mobile Documents/com~apple~CloudDocs/Projects/GardenJournal/manual_prod_run.sh' ubuntu@44.235.31.125:/home/ubuntu/flask_app/
scp -i ~/.ssh/LightsailDefaultKey-us-west-2.pem '/Users/julianbishop/Library/Mobile Documents/com~apple~CloudDocs/Projects/GardenJournal/templates/base.html' ubuntu@44.235.31.125:/home/ubuntu/flask_app/templates/
scp -i ~/.ssh/LightsailDefaultKey-us-west-2.pem '/Users/julianbishop/Library/Mobile Documents/com~apple~CloudDocs/Projects/GardenJournal/templates/index.html' ubuntu@44.235.31.125:/home/ubuntu/flask_app/templates/
scp -i ~/.ssh/LightsailDefaultKey-us-west-2.pem '/Users/julianbishop/Library/Mobile Documents/com~apple~CloudDocs/Projects/GardenJournal/templates/weather.html' ubuntu@44.235.31.125:/home/ubuntu/flask_app/templates/
scp -i ~/.ssh/LightsailDefaultKey-us-west-2.pem '/Users/julianbishop/Library/Mobile Documents/com~apple~CloudDocs/Projects/GardenJournal/events.json' ubuntu@44.235.31.125:/home/ubuntu/flask_app/
scp -i ~/.ssh/LightsailDefaultKey-us-west-2.pem '/Users/julianbishop/Library/Mobile Documents/com~apple~CloudDocs/Projects/GardenJournal/.env' ubuntu@44.235.31.125:/home/ubuntu/flask_app/
scp -i ~/.ssh/LightsailDefaultKey-us-west-2.pem '/Users/julianbishop/Library/Mobile Documents/com~apple~CloudDocs/Projects/GardenJournal/upload_files.sh' ubuntu@44.235.31.125:/home/ubuntu/flask_app/

