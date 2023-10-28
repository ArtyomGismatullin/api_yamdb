from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Category, Genre, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleGetSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        fields = ('username', 'email')
        model = User
    
    def validate_email(self, email):
        if User.objects.exists(email=email):
            raise serializers.ValidationError({'email': 'Email уже используется.'})
        return email

    def validate_username(self, username):
        if User.objects.exists(username=username):
            raise serializers.ValidationError({'username': 'Имя пользователя уже используется.'})
        return username
