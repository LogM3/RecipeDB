from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UserViewSet


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(v1_router.urls))

]
