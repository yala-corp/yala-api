from datetime import timedelta
from django.utils import timezone

from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema

from core.serializers.bid import BidSerializer, BidCreateSerializer
from core.models import Bid, Customer, Auction


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
        seller = Auction.objects.get(pk=request.data["auction"]).seller

        if customer.id == seller.id:
            return Response(
                {"detail": "You can't bid on your own auction"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auction = serializer.validated_data["auction"]

        bids = Bid.objects.filter(auction=auction)
        if bids.count() > 0 and serializer.validated_data["amount"] <= auction.price:
            return Response(
                {"detail": "Price must be higher than the current price"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bid = serializer.save(customer=customer)
        if auction.end_date < timezone.now() + timedelta(minutes=3):
            auction.end_date = timezone.now() + timedelta(minutes=3)

        auction.price = serializer.validated_data["amount"]
        auction.winner = customer
        auction.save()

        return Response(BidSerializer(bid).data, status=status.HTTP_201_CREATED)
