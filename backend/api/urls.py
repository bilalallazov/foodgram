from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    AuthTokenLoginView,
    AuthTokenLogoutView,
    IngredientViewSet,
    RecipeViewSet,
    ResetPasswordView,
    TagViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'auth/token/login/',
        AuthTokenLoginView.as_view(),
        name='auth-login',
    ),
    path(
        'auth/token/logout/',
        AuthTokenLogoutView.as_view(),
        name='auth-logout',
    ),
    path(
        'users/reset_password/',
        ResetPasswordView.as_view(),
        name='reset-password',
    ),
    path('', include(router.urls)),
]
