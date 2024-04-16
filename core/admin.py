from django.contrib import admin
from core.models import Auction, Customer


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
