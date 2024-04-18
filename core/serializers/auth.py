from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from core.models import Customer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
        }


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "password": {"write_only": True},
        }

    def validate(self, data):
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email already exists")
        return data

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        try:
            validate_password(validated_data["password"], user)
        except ValidationError as e:
            raise serializers.ValidationError({"password": str(e)})

        user.set_password(validated_data["password"])
        user.save()

        return user


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True, help_text="User object")
    token = serializers.CharField(help_text="Token string")

    class Meta:
        model = Token
        fields = ["user", "token"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
