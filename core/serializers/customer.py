from rest_framework import serializers
from core.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "document_type",
            "document_number",
            "birth_date",
            "phone_number",
            "address",
            "bank_name",
            "cci",
            "type",
        ]
        extra_kwargs = {
            "type": {"required": True},
            "document_type": {"required": True},
            "document_number": {"required": True},
            "phone_number": {"required": True},
            "address": {"required": True},
        }
