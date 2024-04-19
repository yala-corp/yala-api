from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from core.serializers.auction import AuctionSerializer, AuctionCreateSerializer

from core.models import Auction, Customer


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

    @swagger_auto_schema(
        request_body=AuctionCreateSerializer,
        responses={status.HTTP_201_CREATED: AuctionSerializer},
    )
    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        seller = Customer.objects.get(user=user)
        if seller.type != Customer.SELLER:
            return Response(
                {"error": "Only sellers can create auctions"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AuctionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=seller)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
