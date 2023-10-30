from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from api.filters import CustomTitleFilter
from api.mixins import CreateListDestroyModelMixin
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitleSerializer,
    UserSerializer,
    UserEditSerializer,
    SignupSerializer,
    TokenSerializer,
    ReviewSerializer,
    CommentSerializer
)
from api.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAdminModeratorOwnerOrReadOnly
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=(IsAuthenticated,),
            url_path='me', url_name='my profile')
    def profile(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            serializer = UserEditSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserEditSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateListDestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomTitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitleSerializer


class SignupViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if (User.objects.filter(username=request.data.get('username'),
                                email=request.data.get('email'))):
            user = User.objects.get(username=request.data.get('username'))
            serializer = SignupSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=request.data.get('username'))
        send_mail(
            subject='Код подтверждения.',
            message=f'Твой код: {"confirmation_code"}',
            from_email=None,
            recipient_list=(user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenViewSet(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=request.data.get('username')
        )
        if str('confirmation_code') == request.data.get(
            'confirmation_code'
        ):
            refresh = RefreshToken.for_user(user)
            token = {'token': str(refresh.access_token)}
            return Response(
                token, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorOwnerOrReadOnly
    )

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminModeratorOwnerOrReadOnly
    )

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
