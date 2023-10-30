from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    UserViewSet,
    ReviewViewSet,
    SignupViewSet,
    TitleViewSet,
    TokenViewSet,
)
from api.routers import NoPutRouter

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

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenViewSet.as_view(), name='token'),
    path('v1/auth/signup/', SignupViewSet.as_view(), name='signup'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
