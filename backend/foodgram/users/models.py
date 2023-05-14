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
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(
        max_length=11,
        choices=Role.choices,
        default=Role.USER
    )

    class Meta:
        ordering = ['id']

    @property
    def is_admin(self):
        return self.role == Role.ADMIN


class UserFollow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed'
    )

    def __str__(self):
        return f'{self.user} -> {self.author}'

