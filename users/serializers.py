from users.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class TokenObtainPairResponseSerializer(serializers.Serializer):
    """Token serializer generator."""

    access = serializers.CharField()
    refresh = serializers.CharField()


class SignUpSerializer(serializers.Serializer):
    tokens = TokenObtainPairResponseSerializer(read_only=True)
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "tokens",
        )

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        has_letter = any(char.isalpha() for char in value)
        has_digit = any(char.isdigit() for char in value)
        has_special = any(not char.isalnum() for char in value)

        if not has_letter:
            raise serializers.ValidationError("Password must contain at least one letter.")
        if not has_digit:
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not has_special:
            raise serializers.ValidationError("Password must contain at least one special character.")

        return value

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['tokens'] = instance.tokens
        return rep


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        refresh = RefreshToken.for_user(user)
        return {
            'email': user.email,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



    def to_representation(self, instance):
        return {
            'email': instance.get('email'),
            'access': instance.get('access'),
            'refresh': instance.get('refresh'),
        }
