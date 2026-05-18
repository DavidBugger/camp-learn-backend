#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

if [[ $CREATE_SUPERUSER ]]; then
  python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
email = '$SUPERUSER_EMAIL'
username = '$SUPERUSER_USERNAME'
name = '${SUPERUSER_NAME:-Admin}'
password = '$SUPERUSER_PASSWORD'
if not User.objects.filter(email=email).exists():
    u = User(email=email, username=username, name=name, role='system_admin', is_staff=True, is_superuser=True)
    u.set_password(password)
    u.save()
    print('Superuser created successfully.')
else:
    print('Superuser already exists.')
"
fi
