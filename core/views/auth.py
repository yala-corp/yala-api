from rest_framework import viewsets
from core.serializers.auth import CustomerSerializer
from core.models import Customer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
