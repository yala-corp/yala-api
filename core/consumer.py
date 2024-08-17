# core/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone


class AuctionConsumer(WebsocketConsumer):
    def connect(self):
        print("Connecting")
        self.auction_id = self.scope["url_route"]["kwargs"]["auction_id"]
        self.auction_group_name = f"auction_{self.auction_id}"
        print("conexion con auction", self.auction_id)
        print("grupo", self.auction_group_name)
        print("Conexión establecida channel_name " + self.channel_name)

        async_to_sync(self.channel_layer.group_add)(
            self.auction_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print("Se ha desconectado")
        async_to_sync(self.channel_layer.group_discard)(
            self.auction_group_name, self.channel_name
        )

    def auction_message(self, event):
        message = event["message"]
        Amount = message["price"]
        Date = message["date"]
        Bidder = message["bidder"]
        print("Mensaje de subasta", event)

        self.send(
            text_data=json.dumps({"amount": Amount, "date": Date, "name": Bidder})
        )
        # self.send(text_data=json.dumps({"message": message}))  # con esto se envía el mensaje al websocket conectado, lo recibe el front con onmessage
