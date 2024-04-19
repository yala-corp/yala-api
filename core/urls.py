from rest_framework import routers
from core.views.auth import CustomerViewSet, AuthViewSet
from core.views.auction import AuctionViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register(prefix=r"customers", viewset=CustomerViewSet, basename="customer")

router.register(prefix=r"auth", viewset=AuthViewSet, basename="auth")

router.register(prefix=r"auctions", viewset=AuctionViewSet, basename="auction")

urlpatterns = router.urls
