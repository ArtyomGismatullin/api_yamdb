from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    TokenViewSet,
    SignupViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenViewSet.as_view({'post': 'create'}), name='token'),
    path('v1/auth/signup/', SignupViewSet.as_view({'post': 'create'}), name='signup'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
