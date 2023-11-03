import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
)

User = get_user_model()


def reader(file_name: str):
    csv_path = os.path.join(settings.BASE_DIR, 'static/data/', file_name)
    csv_file = open(csv_path, 'r', encoding='utf-8')
    csv_reader = csv.reader(csv_file, delimiter=',')
    return csv_reader


class Command(BaseCommand):

    def handle(self, *args, **options):
        csv_reader = reader('category.csv')
        next(csv_reader)
        for row in csv_reader:
            _ = Category.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
        print('category: OK')

        csv_reader = reader('genre.csv')
        next(csv_reader, None)
        for row in csv_reader:
            _ = Genre.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
        print('genre: OK')

        csv_reader = reader('titles.csv')
        next(csv_reader, None)
        for row in csv_reader:
            category_obj = get_object_or_404(Category, id=row[3])
            _ = Title.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=category_obj
            )
        print('titles: OK')

        csv_reader = reader('genre_title.csv')
        next(csv_reader, None)
        for row in csv_reader:
            genre_obj = get_object_or_404(Genre, id=row[2])
            title_obj = get_object_or_404(Title, id=row[1])
            _ = GenreTitle.objects.get_or_create(
                id=row[0],
                genre=genre_obj,
                title=title_obj
            )
        print('genre_titles: OK')

        csv_reader = reader('users.csv')
        next(csv_reader, None)
        for row in csv_reader:
            _ = User.objects.get_or_create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            )
        print('users: OK')

        csv_reader = reader('review.csv')
        next(csv_reader, None)
        for row in csv_reader:
            title_obj = get_object_or_404(Title, id=row[1])
            user_obj = get_object_or_404(User, id=row[3])
            _ = Review.objects.get_or_create(
                id=row[0],
                title=title_obj,
                text=row[2],
                author=user_obj,
                score=row[4],
                pub_date=row[5]
            )
        print('reviews - OK')

        csv_reader = reader('comments.csv')
        next(csv_reader, None)
        for row in csv_reader:
            review_obj = get_object_or_404(Review, id=row[1])
            user_obj = get_object_or_404(User, id=row[3])
            _ = Comment.objects.get_or_create(
                id=row[0],
                review=review_obj,
                text=row[2],
                author=user_obj,
                pub_date=row[4]
            )
        print('comments: OK')
