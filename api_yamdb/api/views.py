from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from api.filters import CustomTitleFilter
from api.mixins import CreateListDestroyModelMixin
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleGetSerializer, TitleSerializer,
                             UserSerializer)
from reviews.models import Category, Genre, Title

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=None,
            url_path='me', url_name='My profile')
    def profile(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data)


class CategoryViewSet(CreateListDestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()  # Ошибка. Неоткуда получать рейтинг для произведения
    serializer_class = TitleSerializer
    permission_classes = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomTitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitleSerializer
