release: python manage.py migrate
web: daphne mystore.asgi:application --port $PORT --bind 0.0.0.0