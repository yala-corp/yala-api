from rest_framework import routers
from core.views.auth import AuthViewSet
from core.views.auction import AuctionViewSet
from core.views.customer import CustomerViewSet
from core.views.bid import BidViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register(prefix=r"customers", viewset=CustomerViewSet, basename="customer")

router.register(prefix=r"auth", viewset=AuthViewSet, basename="auth")

router.register(prefix=r"auctions", viewset=AuctionViewSet, basename="auction")

router.register(prefix=r"bids", viewset=BidViewSet, basename="bid")

urlpatterns = router.urls
