from rest_framework import serializers

from reviews.models import Category, Genre, Title, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', read_only=True, many=True
    )
    genre = GenreSerializer(many=True, required=False)

    class Meta:
        model = Title
        fields = ('id', 'title', 'slug', 'description')
