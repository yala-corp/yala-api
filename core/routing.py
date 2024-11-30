# archivo donde se definen las rutas de los websockets

from django.urls import path
from .consumer import AuctionConsumer
from django.urls import re_path

websocket_urlpatterns = [
    path(
        "ws/auctions/<uuid:auction_id>/", AuctionConsumer.as_asgi()
    ),  # se define la ruta del websocket
]
