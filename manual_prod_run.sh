cd /home/ubuntu/flask_app
source venv/bin/activate
gunicorn --workers 3 --bind 0.0.0.0:8080 app:app --log-level debug
