from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models

from api.validators import get_current_year


class CategoryGenre(models.Model):
    name = models.CharField('Название', max_length=settings.LIMIT_NAME)
    slug = models.SlugField(
        'Уникальный идентификатор',
        max_length=settings.LIMIT_SLUG,
        unique=True,
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(CategoryGenre):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenre):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField('Название', max_length=settings.LIMIT_NAME)
    year = models.PositiveIntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(get_current_year)]
    )
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
