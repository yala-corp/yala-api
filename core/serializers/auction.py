from rest_framework import serializers
from core.models import Auction, AuctionImage


class AuctionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionImage
        fields = ["image", "uploaded_at"]



class AuctionSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="seller.user.first_name", read_only=True)
    last_name = serializers.CharField(source="seller.user.last_name", read_only=True)
    email = serializers.EmailField(source="seller.user.email", read_only=True)
    images = AuctionImageSerializer(many=True)

    class Meta:
        model = Auction
        fields = "__all__"


class AuctionCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

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
            "state",
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
            "state": {"required": True},
            "images": {"required": True},
        }
