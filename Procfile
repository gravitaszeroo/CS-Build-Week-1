release: python manage.py makemigrations
release: python manage.py migrate
release: python manage.py shell < util/room_generator.py
web: gunicorn adv_project.wsgi:application --log-file -