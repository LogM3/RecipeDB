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
        validators=[UnicodeUsernameValidator],
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    role = models.CharField(
        max_length=11,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == Role.ADMIN


class UserFollow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed',
        verbose_name='Пользователь'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Подписка на пользователя'
        verbose_name_plural = 'Подписки на пользователей'
        constraints = [models.UniqueConstraint(
            fields=['author', 'user'],
            name='Unique UserFollow'
        )]

    def __str__(self):
        return f'{self.user} -> {self.author}'
