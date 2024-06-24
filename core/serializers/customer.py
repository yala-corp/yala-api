from rest_framework import serializers
from core.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "document_number",
            "birth_date",
            "bank_name",
            "cci",
            "address",
            "phone_number",
        ]
        extra_kwargs = {
            "document_number": {"required": True},
            "birth_date": {"required": True},
            "bank_name": {"required": True},
            "cci": {"required": True},
            "address": {"required": True},
        }


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
        ]
        extra_kwargs = {
            "document_type": {"required": True},
            "document_number": {"required": True},
            "phone_number": {"required": True},
            "address": {"required": True},
        }


class CustomerUpdateSerializer(serializers.ModelSerializer):
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
        ]


class CustomerVerificationSerializer(serializers.Serializer):
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    VERIFICATION_NAME_CHOICES = [
        (EMAIL, "Email"),
        (PHONE, "Phone"),
    ]
    verification_code = serializers.CharField(
        max_length=6, help_text="Verification code"
    )
    verification_name = serializers.ChoiceField(
        choices=VERIFICATION_NAME_CHOICES, help_text="Verification name"
    )
