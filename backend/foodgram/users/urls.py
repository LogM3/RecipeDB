from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserFollowsViewSet

router = DefaultRouter()
router.register('users', UserFollowsViewSet, 'users')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
