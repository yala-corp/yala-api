from rest_framework import serializers
from core.models import Auction


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = "__all__"


class AuctionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = [
            "title",
            "description",
            "starting_price",
            "price",
            "start_date",
            "end_date",
            "image",
            "category",
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
        }
