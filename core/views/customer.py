from datetime import timedelta
from django.utils import timezone

from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema
from core.utils import send_phone_verification, generate_verification_code
from core.exceptions import EmailServiceError

from core.models import Customer
from core.serializers.customer import (
    CustomerSerializer,
    CustomerCreateSerializer,
    CustomerUpdateSerializer,
    CustomerVerificationSerializer,
)
from core.serializers.auction import AuctionSerializer


class CustomerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=CustomerCreateSerializer,
        responses={status.HTTP_201_CREATED: CustomerSerializer},
    )
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=CustomerUpdateSerializer,
        responses={status.HTTP_200_OK: CustomerSerializer},
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CustomerUpdateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        customer: Customer = serializer.save()

        if not customer.validated_phone and customer.phone_number:
            try:
                verification_code = generate_verification_code()
                send_phone_verification(
                    phone_number=customer.phone_number,
                    verification_code=verification_code,
                )
                customer.verification_code = verification_code
                customer.verification_code_expiry = timezone.now() + timedelta(
                    minutes=30
                )
                customer.save()
            except Exception as e:
                raise EmailServiceError({"detail": str(e)})

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CustomerSerializer})
    @action(methods=["GET"], detail=False)
    def user(self, request, *args, **kwargs):
        user = request.user
        customer = Customer.objects.get(user=user)
        return Response(CustomerSerializer(customer).data)

    @swagger_auto_schema(
        methods=["POST"],
        request_body=CustomerVerificationSerializer,
        responses={status.HTTP_200_OK: CustomerSerializer},
    )
    @action(methods=["POST"], detail=False)
    def verify(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomerVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = Customer.objects.get(user=user)

        verification_code = serializer.validated_data["verification_code"]
        verification_name = serializer.validated_data["verification_name"]

        if verification_name == CustomerVerificationSerializer.EMAIL:
            if customer.verification_code != verification_code:
                return Response(
                    {"error": "Invalid verification code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            customer.verification_code = None
            customer.validated_email = True
        elif verification_name == CustomerVerificationSerializer.PHONE:
            if customer.verification_code != verification_code:
                return Response(
                    {"error": "Invalid verification code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            customer.verification_code = None
            customer.validated_phone = True
        else:
            return Response(
                {"error": "Invalid verification name"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        customer.save()

        return Response(CustomerSerializer(customer).data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: AuctionSerializer(many=True)},
    )
    @action(methods=["GET"], detail=False)
    def auctions(self, request, *args, **kwargs):
        customer = request.user.customer
        auctions = customer.auctions_sold.all()
        serializer = AuctionSerializer(auctions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
