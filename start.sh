python3 manage.py migrate
python3 manage.py collectstatic
gunicorn fine_project.wsgi:application --workers 3 -b 0.0.0.0:8000 --access-logfile ~/FinE/gunicorn_access.log --error-logfile ~/FinE/gunicorn_error.log 
