import uuid
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    BUYER = "BUYER"
    SELLER = "SELLER"
    USER_TYPE_CHOICES = [
        (BUYER, "Buyer"),
        (SELLER, "Seller"),
    ]
    DNI = "DNI"
    RUC = "RUC"
    PASSPORT = "PASSPORT"
    DOCUMENT_TYPE_CHOICES = [
        (DNI, "DNI"),
        (RUC, "RUC"),
        (PASSPORT, "Passport"),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, help_text="Associated user"
    )
    document_type = models.CharField(
        max_length=9,
        choices=DOCUMENT_TYPE_CHOICES,
        default=DNI,
        help_text="Customer document type",
    )
    document_number = models.CharField(
        max_length=15, help_text="Customer document number"
    )
    birth_date = models.DateField(
        blank=True, null=True, help_text="Customer birth date"
    )
    phone_number = models.CharField(max_length=10, help_text="Customer phone number")
    address = models.CharField(max_length=100, help_text="Customer address")
    cci = models.CharField(
        max_length=24, blank=True, null=True, help_text="Customer CCI number"
    )
    bank_name = models.CharField(
        max_length=32, blank=True, null=True, help_text="Customer bank name"
    )
    type = models.CharField(
        max_length=6,
        choices=USER_TYPE_CHOICES,
        default=BUYER,
        help_text="Customer type",
    )


class Auction(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, help_text="Auction ID"
    )
    title = models.CharField(max_length=100, help_text="Product name")
    description = models.TextField(help_text="Product description")
    starting_price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Starting price"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Final price"
    )
    start_date = models.DateTimeField(help_text="Auction start date")
    end_date = models.DateTimeField(help_text="Auction end date")
    winner = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="auctions_won",
        help_text="Auction winner",
        blank=True,
    )
    seller = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="auctions_sold",
        help_text="Auction seller",
    )
