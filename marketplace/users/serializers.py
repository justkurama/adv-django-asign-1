from rest_framework import serializers
from .models import CustomUser, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'profile_image']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nesting user details

    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role', 'profile_image']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)  # Create profile on user creation
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        from rest_framework_simplejwt.tokens import RefreshToken

        user = authenticate(**data)
        if user:
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
        raise serializers.ValidationError("Invalid credentials")
