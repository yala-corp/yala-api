from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema

from core.models import Customer
from core.serializers.customer import CustomerSerializer, CustomerCreateSerializer


class CustomerViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=CustomerCreateSerializer,
        responses={status.HTTP_201_CREATED: CustomerSerializer},
    )
    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
