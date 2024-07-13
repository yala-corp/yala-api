from rest_framework import serializers
from core.models import Bid


class AuctionBidSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="customer.user.first_name", read_only=True)
    date = serializers.DateTimeField(required=True, help_text="Bid date")

    class Meta:
        model = Bid
        fields = ["amount", "date", "name"]


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = "__all__"


class BidCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = [
            "amount",
            "auction",
        ]
        extra_kwargs = {
            "amount": {"required": True},
            "auction": {"required": True},
        }

    def validate(self, data):
        if data["amount"] < data["auction"].price:
            raise serializers.ValidationError(
                "Price must be higher than the current price"
            )
        return data
