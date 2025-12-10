from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.users.serializers.user_auth_serializer import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        data = {
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ListUserView(generics.ListAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()