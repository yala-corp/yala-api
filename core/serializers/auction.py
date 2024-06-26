from rest_framework import serializers
from core.models import Auction
from core.serializers.auctionimage import AuctionImageSerializer


class AuctionSerializer(serializers.ModelSerializer):
    images = AuctionImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Auction
        fields = "__all__"


class AuctionCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True
    )
    
    class Meta:
        model = Auction
        fields = [
            "title",
            "description",
            "starting_price",
            "price",
            "start_date",
            "end_date",
            "category",
            "estado",
            "images",
        ]
        extra_kwargs = {
            "title": {"required": True},
            "description": {"required": True},
            "starting_price": {"required": True},
            "price": {"required": True},
            "start_date": {"required": True},
            "end_date": {"required": True},
            "image": {"required": True},
            "category": {"required": True},
            "estado": {"required": True},
            "images": {"required": True},
        }

    