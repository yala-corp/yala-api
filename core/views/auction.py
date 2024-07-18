from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.serializers.auction import AuctionSerializer, AuctionCreateSerializer
from core.serializers.bid import AuctionBidSerializer
from core.models import Auction, Customer, AuctionImage, Bid


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

    # def get_parser_classes(self):
    #     if self.action == 'create':
    #         return [MultiPartParser, FormParser]
    #     return super().get_parser_classes()

    # @swagger_auto_schema(
    #     request_body=AuctionCreateSerializer,
    #     responses={status.HTTP_201_CREATED: AuctionSerializer},
    # )
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'starting_price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL),
                'start_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                'end_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                'category': openapi.Schema(type=openapi.TYPE_STRING),
                'state': openapi.Schema(type=openapi.TYPE_STRING),
                'images': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY))
            },
            required=['title', 'description', 'starting_price', 'price', 'start_date', 'end_date', 'category', 'state', 'images']
        ),
        responses={status.HTTP_201_CREATED: AuctionSerializer},
    )
    def create(self, request, *args, **kwargs):
        user = request.user
        seller = Customer.objects.get(user=user)
        winner = seller

        serializer = AuctionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        images = serializer.validated_data.pop("images")

        auction = serializer.save(seller=seller, winner=winner)

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

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: AuctionBidSerializer(many=True)}
    )
    @action(methods=["GET"], detail=True)
    def bids(self, request, *args, **kwargs):
        auction = self.get_object()
        bids = Bid.objects.filter(auction=auction).order_by("-date")
        serializer = AuctionBidSerializer(bids, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
