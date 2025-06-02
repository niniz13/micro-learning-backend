import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'micro_learning.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser(email='admin@example.com', password='admin', first_name='Admin', last_name='User')

if not User.objects.filter(email='user@example.com').exists():
    User.objects.create_user(email='user@example.com', password='user', first_name='Basic', last_name='User')


