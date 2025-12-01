from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken



User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    
    
    class Meta:
        model = User
        fields = ('id','username', 'phone', 'password', 'first_name', 'last_name', 'email')
        
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    
    def validate(self, data):
        from django.contrib.auth import authenticate
        
        user = authenticate(username=data['username'], password = data['password'])
        
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        
        
        refresh = RefreshToken.for_user(user)
        
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        
        
 