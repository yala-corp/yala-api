from rest_framework import routers
from core.views.auth import CustomerViewSet, AuthViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register(prefix=r"customers", viewset=CustomerViewSet, basename="customer")

router.register(prefix=r"auth", viewset=AuthViewSet, basename="auth")

urlpatterns = router.urls
