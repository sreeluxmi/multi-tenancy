from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet
from django_tenants.utils import get_public_schema_name

from .models import User
from .serializers import UserSerializer, UserLoginSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_authenticated:
            return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLoginAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            print(username)
            password = serializer.validated_data['password']
            print(password)

            user = User.objects.filter(username=username).first()
            print("user", user)

            if user is None or not user.check_password(password):
                return Response({'detail': 'Invalid credentials'},
                                status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({'access_token': access_token}, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


