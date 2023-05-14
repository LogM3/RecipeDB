from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from .models import User, UserFollow
from .serializers import CustomUserSerializerWithRecipes as UserSerializer


class UserFollowsViewSet(UserViewSet):
    @action(methods=['POST', 'DELETE'], detail=True)
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        is_subscribed = (
            UserFollow.objects.filter(
                user=user,
                author=author
            ).exists() or user == author
        )
        if request.method == 'POST':
            if is_subscribed:
                return Response(
                    'You are already subscribed to this user',
                    status=HTTP_400_BAD_REQUEST
                )
            UserFollow.objects.create(user=user, author=author)
            return Response(
                UserSerializer(author, context={'request': request}).data,
                HTTP_201_CREATED
            )

        if not is_subscribed:
            return Response(
                'You are not subscribed to this user',
                status=HTTP_400_BAD_REQUEST
            )
        with atomic():
            UserFollow.objects.filter(user=user, author=author).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False)
    def subscriptions(self, request):
        return self.get_paginated_response(
            UserSerializer(
                self.paginate_queryset(
                    User.objects.filter(subscribers__user=request.user)
                ),
                many=True,
                context={'request': request}
            ).data
        )
