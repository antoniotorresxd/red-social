# apps/users/test.py
import json
from .models import User
from django.contrib.auth.hashers import make_password

def run():
    with open('usuarios_ficticios.json') as f:
        users = json.load(f)

    hashed_pw = make_password('12345678')
    data = [
        User(
            email=u['fields']['email'],
            name=u['fields']['name'],
            birthdate=u['fields']['birthdate'],
            id_student=u['fields']['id_student'],
            password=hashed_pw
        )
        for u in users
    ]

    User.objects.bulk_create(data, batch_size=500)
    print(f"✅ {len(data)} usuarios creados exitosamente.")
