import secrets
import string

from django.db import models
from django.contrib.postgres.fields import ArrayField

TYPE_CHOICES = [
    ('forum', 'Foro'),
    ('group', 'Grupo'),
]

class Community(models.Model):
    admin_id = models.IntegerField()
    name = models.CharField(unique=True)
    code = models.CharField(max_length=7, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    list_users = ArrayField(models.IntegerField(), default=list, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def generate_code(length: int = 7) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
        
    def join_community(self, user_id: int):
        if user_id not in self.list_users:
            self.list_users.append(user_id)
            self.save(update_fields=['list_users'])
        return self

    def exit_community(self, user_id: int):
        if user_id in self.list_users:
            self.list_users.remove(user_id)
            self.save(update_fields=['list_users'])
        return self

    def get_participants(self):
        return self.list_users
    