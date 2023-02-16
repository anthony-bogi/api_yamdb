from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    SignUpViewSet,
    token,
)

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'auth/signup', SignUpViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/token/', token, name='token'),
]
