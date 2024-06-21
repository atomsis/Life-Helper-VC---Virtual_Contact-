# -------- Actually Version ------------------------
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'chat_{self.room_name}'
        print(f"Connecting to room: {self.room_group_name}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(f"Disconnecting from room: {self.room_group_name}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_username = text_data_json['sender']

        sender = await self.get_user_by_username(sender_username)
        recipient = await self.get_user_by_id(int(self.room_name))

        Message.objects.create(sender=sender, recipient=recipient, message=message)
        print(f"Message received: {message} from {sender.username} to {recipient.username}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender.id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sender = await self.get_username(sender_id)
        print(f"Sending message: {message} from {sender}")

        await self.send(text_data=json.dumps({
            'event': 'Send',
            'message': message,
            'sender': sender
        }))

    async def get_user_by_username(self, username):
        return await sync_to_async(User.objects.get)(username=username)

    async def get_user_by_id(self, user_id):
        return await sync_to_async(User.objects.get)(id=user_id)

    async def get_username(self, user_id):
        user = await self.get_user_by_id(user_id)
        return user.username
#--------------------------------------------------------------------



# -------- Not Actually Version ------------------------
# # chat/consumers.py
# import json
# from channels.generic.websocket import WebsocketConsumer
# from .models import Message
# from django.contrib.auth.models import User
#
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['username']
#         self.room_group_name = f'chat_{self.room_name}'
#
#         self.accept()
#
#     def disconnect(self, close_code):
#         pass
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         sender_username = text_data_json['sender']
#
#         sender = User.objects.get(username=sender_username)
#         recipient = User.objects.get(username=self.room_name)
#
#         Message.objects.create(sender=sender, recipient=recipient, message=message)
#
#         self.send(text_data=json.dumps({
#             'message': message,
#             'sender': sender.username
#         }))
#--------------------------------------------------------------------

