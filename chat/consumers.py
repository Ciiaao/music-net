import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model
from notifications.models import Notification
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (Frontend JS)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        recipient_username = text_data_json.get('recipient') # <-- ADD THIS
        username = self.scope['user'].username

        # Pass the recipient to the database function
        await self.save_message(username, self.room_name, message, recipient_username)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group and send it to WebSocket
# Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        attachment = event.get('attachment', None) # Add this line to grab the attachment

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'attachment': attachment # Send it to the frontend HTML!
        }))

    @database_sync_to_async
    def save_message(self, username, room_name, message, recipient_username=None):
        sender = User.objects.get(username=username)
        Message.objects.create(sender=sender, room_name=room_name, content=message)
        
        # If this is a private chat, send a notification to the other person!
        if recipient_username:
            try:
                recipient = User.objects.get(username=recipient_username)
                # Only notify if they aren't talking to themselves
                if sender != recipient:
                    Notification.objects.create(
                        recipient=recipient,
                        sender=sender,
                        notification_type='message',
                        text_preview=message[:50] # Snippet of the chat message
                    )
            except User.DoesNotExist:
                pass