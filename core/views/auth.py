from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from core.serializers.auth import (
    CustomerSerializer,
    UserCreateSerializer,
    TokenSerializer,
)
from core.models import Customer


class AuthViewSet(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer

    @action(methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        pass

    @swagger_auto_schema(
        methods=["POST"],
        request_body=UserCreateSerializer,
        responses={status.HTTP_200_OK: TokenSerializer},
    )
    @action(methods=["POST"], detail=False, serializer_class=UserCreateSerializer)
    def register(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response(TokenSerializer(token).data)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
