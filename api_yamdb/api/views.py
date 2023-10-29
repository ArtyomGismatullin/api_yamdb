from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, generics, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title
from api.filters import CustomTitleFilter
from api.mixins import CreateListDestroyModelMixin
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitleSerializer,
    UserSerializer,
    SignupSerializer,
    TokenSerializer
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

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=(IsAuthenticated,),
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
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomTitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitleSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def get_signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=f'Твой код: {confirmation_code}',
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
