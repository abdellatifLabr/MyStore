release: python src/manage.py migrate
web: gunicorn --pythonpath src mystore.wsgi --preload --log-file -