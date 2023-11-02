from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from api.routers import NoPutRouter
from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    SignupViewSet,
    TitleViewSet,
    TokenViewSet,
    UserViewSet,
)

app_name = 'api'

router = NoPutRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')
router.register('users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urls = [
    path(
        'signup/', SignupViewSet.as_view(), name='signup',
    ),
    path(
        'token/', TokenViewSet.as_view(), name='token'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(), name='token_refresh'
    ),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urls)),
]
