python3 manage.py migrate
python3 manage.py collectstatic
gunicorn --workers 3 -b 0.0.0.0:8000 fine_project.wsgi:application --access-logfile /proj/gunicorn_access.log --error-logfile /proj/gunicorn_error.log
