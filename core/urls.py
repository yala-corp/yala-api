from rest_framework import routers
from core.views.auth import CustomerViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register(
    prefix=r"customers",
    viewset=CustomerViewSet,
    basename="customer"
)

urlpatterns = router.urls
