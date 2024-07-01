from rest_framework import serializers
from core.models import Bid
from datetime import datetime

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = "__all__"

class BidCreateSerializer(serializers.ModelSerializer):
    auction_start_date = serializers.DateTimeField(source='auction.start_date', read_only=True)
    auction_end_date = serializers.DateTimeField(source='auction.end_date', read_only=True)

    class Meta:
        model = Bid
        fields = [
            "amount",
            "auction",
            "auction_start_date",
            "auction_end_date",
        ]
        extra_kwargs = {
            "amount": {"required": True},
            "auction": {"required": True},
        }

    def validate(self, data):
        
        if data["amount"] <= data["auction"].price:
            raise serializers.ValidationError(
                "El precio tiene que ser mayor al precio actual"
            )
        
        
        if data["auction"].end_date < datetime.now():
            raise serializers.ValidationError(
                "No puedes hacer una oferta despues que la subasta termino."
            )
        
        return data