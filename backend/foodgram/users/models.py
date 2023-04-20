from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class Role(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator]
    )
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    role = models.CharField(
        max_length=11,
        choices=Role.choices,
        default=Role.USER
    )
    confirmation_code = models.CharField(
        max_length=40,
        editable=False,
        default=str(uuid4())
    )

    class Meta:
        ordering = ['id']

    @property
    def is_admin(self):
        return self.role == Role.ADMIN
