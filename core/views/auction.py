from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema

from core.serializers.auction import AuctionSerializer, AuctionCreateSerializer
from core.models import Auction, Customer, AuctionImage


class AuctionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        request_body=AuctionCreateSerializer,
        responses={status.HTTP_201_CREATED: AuctionSerializer},
    )
    def create(self, request, *args, **kwargs):
        user = request.user
        seller = Customer.objects.get(user=user)
        winner = seller

        serializer = AuctionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        images = serializer.validated_data.pop("images")

        auction = serializer.save(seller=seller)

        for image in images:
            AuctionImage.objects.create(auction=auction, image=image)

        serializer = AuctionSerializer(auction)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=AuctionSerializer,
        responses={status.HTTP_200_OK: AuctionSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        user = request.user
        seller = instance.seller.user
        if user != seller:
            raise PermissionDenied("Only the seller can update the auction.")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)
