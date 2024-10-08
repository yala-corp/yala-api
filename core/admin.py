from django.contrib import admin
from core.models import Auction, Customer, AuctionImage, Bid


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(AuctionImage)
class AuctionImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", "customer", "amount", "date")
