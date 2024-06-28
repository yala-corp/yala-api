from rest_framework import serializers
from core.models import AuctionImage


class AuctionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionImage
        fields = ["image", "uploaded_at"]
