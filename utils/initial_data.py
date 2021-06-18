from django.conf import settings
from users.models import User


def add_users(apps, schema_editor, **context):
    data = {
        'email': settings.SA_EMAIL,
        'first_name': settings.SA_FIRST_NAME,
        'last_name': settings.SA_LAST_NAME,
        'password': settings.SA_PASSWORD
    }
    errors = False
    cont = 0
    print('Adding users...')
    try:
        User.objects.create_superuser(**data)
        cont += 1
    except Exception as e:
        errors = True
        print(f" Error adding user '{data['email']}': {str(e)}")

    if not errors:
        print(f"'{cont}' users added.")
