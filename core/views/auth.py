from random import randint

from datetime import timedelta
from django.utils import timezone

from django.core.mail import send_mail

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from core.serializers.auth import (
    UserCreateSerializer,
    UserLoginSerializer,
    TokenSerializer,
)

from core.exceptions import EmailServiceError
from core.models import Customer


def generate_verification_code():
        return str(randint(100000, 999999))


class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = AuthTokenSerializer

    @swagger_auto_schema(
        methods=["POST"],
        request_body=UserLoginSerializer,
        responses={status.HTTP_200_OK: TokenSerializer},
    )
    @action(methods=["POST"], detail=False, serializer_class=UserLoginSerializer)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(TokenSerializer(token).data)

    @swagger_auto_schema(
        methods=["POST"],
        request_body=UserCreateSerializer,
        responses={status.HTTP_200_OK: TokenSerializer},
    )
    @action(methods=["POST"], detail=False, serializer_class=UserCreateSerializer)
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.save()
            verification_code = generate_verification_code()

            send_mail(
                subject=f"Bienvenido a Yala",
                message=f"Gracias por registrarte en Yala, tu código de verificación es {verification_code}",
                from_email="settings.EMAIL_HOST_USER",
                recipient_list=[serializer.validated_data["email"]],
                fail_silently=False,
            )

            _ = Customer.objects.create(
                user=user,
                verification_code=verification_code,
                verification_code_expiry=timezone.now() + timedelta(minutes=30),
            )
        except Exception as e:
            print(e)
            raise EmailServiceError({"detail": str(e)})

        token, _ = Token.objects.get_or_create(user=user)

        return Response(TokenSerializer(token).data)
