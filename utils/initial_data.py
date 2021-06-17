from users.models import User


def add_users(apps, schema_editor, **context):
    data = {
        'email': 'naranjo.chuy@gmail.com',
        'first_name': 'Chuy',
        'last_name': 'Naranjo',
        'password': '123456'
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
