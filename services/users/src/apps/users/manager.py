from django.core.validators import validate_email
from django.contrib.auth.models import BaseUserManager
from django.db import transaction

class AccountManager(BaseUserManager):
    def create_user(self, email, name, password, birthdate, **extra_fields):
        validate_email(email)
        with transaction.atomic():
            user = self.model(
                email=self.normalize_email(email),
                name=name,
                birthdate=birthdate,
                **extra_fields
            )
            user.set_password(password)
            user.save(using=self._db)
            return user

    def update_user(self, user, name=None, email=None, birthdate=None, id_student=None):
        if email:
            validate_email(email)
            user.email = self.normalize_email(email)
        if name:
            user.name = name
        if birthdate:
            user.birthdate = birthdate
        if id_student is not None:
            user.id_student = id_student
        user.save(using=self._db)
        return user
