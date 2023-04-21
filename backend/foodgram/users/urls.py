from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UserViewSet, token_obtain, user_info


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/token/login/', token_obtain, name='token_obtain'),
    path('users/me/', user_info, name='user_info'),
    path('', include(v1_router.urls))

]
