from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb import settings


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICE = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.LIMIT_USERNAME,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Недоступный символ для имени пользователя!'
        )])
    email = models.EmailField(
        'Электронная почта',
        max_length=settings.LIMIT_EMAIL,
        unique=True
    )
    first_name = models.CharField(
        'Имя', blank=True, max_length=settings.LIMIT_USERNAME)
    last_name = models.CharField(
        'Фамилия', blank=True, max_length=settings.LIMIT_USERNAME)
    bio = models.TextField('О себе', blank=True)
    role = models.CharField(
        'Роль',
        max_length=settings.LIMIT_USERNAME,
        choices=ROLE_CHOICE,
        default=USER,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
