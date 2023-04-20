from rest_framework.viewsets import ModelViewSet
from backend.foodgram.core.paginators import CustomPagination

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
        else:
            return [IsAdmin()]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        else:
            return UserSerializer

