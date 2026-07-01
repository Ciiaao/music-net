release: python manage.py migrate --noinput
web: python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p $PORT musicPlatform.asgi:application
