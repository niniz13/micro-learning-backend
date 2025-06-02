PORT=${PORT:-10000}

python manage.py migrate --noinput
python create_superuser.py
exec gunicorn micro_learning.wsgi:application --bind 0.0.0.0:$PORT