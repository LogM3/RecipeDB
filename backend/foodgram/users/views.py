from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from backend.foodgram.core.paginators import CustomPagination
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, CreateUserSerializer
from .models import User
from .permissions import IsAdmin


# class UserSignupAPIView(APIView):
#     def post(self, request):
#         serializer = CreateUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data.get('username')
#         email = serializer.validated_data.get('email')
#         first_name = serializer.validated_data.get('first_name')
#         last_name = serializer.validated_data.get('last_name')
#         password = serializer.validated_data.get('password')
#         user, created = User.objects.get_or_create(
#             username=username,
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             password=password
#         )
#         return Response(serializer.data, status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'create':
            return super().get_permissions()
        elif self.action == 'retrieve':
            return [IsAuthenticated()]
        else:
            return [IsAdmin()]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        else:
            return UserSerializer


@api_view(['POST'])
def token_obtain(request):
    serializer = TokenObtainSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token = RefreshToken.for_user(get_object_or_404(
        User, username=request.data.get('username'))
    )
    return Response({'token': str(token.access_token)}, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_info(request):
    return Response(
        UserSerializer(get_object_or_404(User, pk=request.user.pk)).data
    )

