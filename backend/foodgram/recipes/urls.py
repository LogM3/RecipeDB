from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet


router = DefaultRouter()
router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls))
]
