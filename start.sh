python3 manage.py migrate
gunicorn fine_project.wsgi:application -b 0.0.0.0:8000 --timeout 120