from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        extra_kwargs = {
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
        }


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email of the user")
    password = serializers.CharField(help_text="Password of the user")

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = User.objects.filter(email=email).first()

            if user:
                if user.check_password(password):
                    return {"user": user}
            raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Email and password are required")


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        extra_kwargs = {
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "password": {"write_only": True},
        }

    def validate(self, data):
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email already exists")
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("Username already exists")
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        try:
            validate_password(validated_data["password"], user)
        except ValidationError as e:
            raise serializers.ValidationError(" ".join(e.messages))

        user.set_password(validated_data["password"])
        user.save()

        return user


class UserGoogleSerializer(serializers.Serializer):
    name = serializers.CharField(help_text="Name of the user")
    email = serializers.EmailField(help_text="Email of the user")

    def validate(self, data):
        email = data.get("email")

        if not email:
            raise serializers.ValidationError("Email is required")

        return data

    def create_or_get_user(self, validated_data):
        user = User.objects.filter(email=validated_data["email"]).first()
        if user:
            return user, False
        user = User(
            username=validated_data["name"],
            email=validated_data["email"],
            first_name=validated_data["name"],
        )
        user.save()
        return user, True


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True, help_text="User object")

    class Meta:
        model = Token
        fields = ["user", "key"]
