from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField('Заголовок', max_length=256)
    slug = models.SlugField(
        'Slug категории',
        max_length=50,
        unique=True,
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        'Slug жанра',
        max_length=50,
        unique=True,
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.PositiveIntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True)
    genres = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
