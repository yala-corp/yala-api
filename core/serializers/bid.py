from rest_framework import serializers
from core.models import Bid


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
