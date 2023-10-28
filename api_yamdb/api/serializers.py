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
