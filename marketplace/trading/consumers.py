import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Order

class OrderBookConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("order_book", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("order_book", self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send("order_book", {"type": "send_update"})

    async def send_update(self, event):
        orders = list(Order.objects.filter(status="pending").values())
        await self.send(text_data=json.dumps({"orders": orders}))
