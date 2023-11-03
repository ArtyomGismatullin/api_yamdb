from django.contrib import admin

from reviews.models import (
    Category, Comment, Genre, GenreTitle, Review, Title, User
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'get_genre',
    )
    list_filter = ('name',)
    search_fields = ('name', 'year', 'category')
    list_editable = ('category',)

    def get_genre(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])
    get_genre.short_description = 'Жанры'


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'genre', 'title')
    list_filter = ('genre',)
    search_fields = ('title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'text',
        'score',
        'pub_date',
        'title'
    )
    list_filter = ('author', 'score', 'pub_date')
    search_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'pub_date', 'review')
    list_filter = ('author', 'pub_date')
    search_fields = ('author',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'role'
    )
    list_editable = ('role',)
    list_filter = ('username',)
    search_fields = ('username', 'role')
