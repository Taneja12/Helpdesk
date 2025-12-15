from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_USER = 'user'
    ROLE_AGENT = 'agent'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = (
        (ROLE_USER, 'User'),
        (ROLE_AGENT, 'Agent'),
        (ROLE_ADMIN, 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def name_email(self):
        name = f"{self.first_name} {self.last_name}".strip()
        if name:
            return f"{name} - {self.email}"
        return self.email
