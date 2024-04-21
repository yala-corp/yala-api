from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema

from core.serializers.bid import BidSerializer, BidCreateSerializer

from core.models import Bid, Customer


class BidViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bid.objects.filter(customer=self.request.user.customer)

    @swagger_auto_schema(
        request_body=BidCreateSerializer,
        responses={status.HTTP_201_CREATED: BidSerializer},
    )
    def create(self, request, *args, **kwargs):
        customer = request.user.customer

        if customer.type != Customer.BUYER:
            return Response(
                {"error": "Only buyers can create bids"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer)

        auction = serializer.validated_data["auction"]
        auction.price = serializer.validated_data["amount"]
        auction.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
