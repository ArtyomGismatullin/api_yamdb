from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models


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
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Недоступный символ для имени пользователя!'
            ),
            RegexValidator(
                regex=r'^me$',
                inverse_match=True,
                message='Имя пользователя "me" недопустимо'
            )])
    email = models.EmailField(
        'Электронная почта',
        max_length=settings.LIMIT_EMAIL,
        unique=True
    )
    bio = models.TextField('О себе', blank=True)
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role, _ in ROLE_CHOICE),
        choices=ROLE_CHOICE,
        default=USER,
    )

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
