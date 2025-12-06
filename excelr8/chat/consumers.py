import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils import timezone
from .models import ChatRoom, ChatMessage, RoomMembership
import re


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']
        
        # Check if user is authenticated
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Check if user is a member of this room
        is_member = await self.check_room_membership()
        if not is_member:
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Set user as online
        await self.set_user_online(True)
        
        # Send message history
        messages = await self.get_message_history()
        await self.send(text_data=json.dumps({
            'type': 'message_history',
            'messages': messages
        }))
        
        # Notify others that user joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'username': self.user.username,
                'status': 'joined',
                'online_users': await self.get_online_users()
            }
        )
    
    async def disconnect(self, close_code):
        # Set user as offline
        await self.set_user_online(False)
        
        # Notify others that user left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'username': self.user.username,
                'status': 'left',
                'online_users': await self.get_online_users()
            }
        )
        
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()
        
        if not message:
            return
        
        # Handle commands
        if message.startswith('/'):
            await self.handle_command(message)
            return
        
        # Save message to database
        saved_message = await self.save_message(message)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
                'timestamp': saved_message['timestamp'],
                'message_id': saved_message['id']
            }
        )
    
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id']
        }))
    
    async def user_status(self, event):
        # Send user status update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'username': event['username'],
            'status': event['status'],
            'online_users': event['online_users']
        }))
    
    async def system_message(self, event):
        # Send system message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'system_message',
            'message': event['message']
        }))
    
    async def handle_command(self, command):
        cmd = command.lower().strip()
        
        if cmd == '/help':
            help_text = """
Available Commands:
/help - Show this help message
/users - List all users in this room
@username - Mention a user in your message
            """.strip()
            await self.send(text_data=json.dumps({
                'type': 'system_message',
                'message': help_text
            }))
        
        elif cmd == '/users':
            online_users = await self.get_online_users()
            all_members = await self.get_all_members()
            
            users_text = f"Users in this room:\n"
            users_text += f"Online ({len(online_users)}): {', '.join(online_users)}\n"
            
            offline = [u for u in all_members if u not in online_users]
            if offline:
                users_text += f"Offline ({len(offline)}): {', '.join(offline)}"
            
            await self.send(text_data=json.dumps({
                'type': 'system_message',
                'message': users_text
            }))
        
        else:
            await self.send(text_data=json.dumps({
                'type': 'system_message',
                'message': f'Unknown command: {command}. Type /help for available commands.'
            }))
    
    @database_sync_to_async
    def check_room_membership(self):
        try:
            room = ChatRoom.objects.get(id=self.room_id, is_active=True)
            membership = RoomMembership.objects.filter(
                user=self.user,
                room=room
            ).exists()
            return membership
        except ChatRoom.DoesNotExist:
            return False
    
    @database_sync_to_async
    def set_user_online(self, is_online):
        try:
            membership = RoomMembership.objects.get(
                user=self.user,
                room_id=self.room_id
            )
            membership.is_online = is_online
            membership.save()
        except RoomMembership.DoesNotExist:
            pass
    
    @database_sync_to_async
    def get_message_history(self, limit=100):
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            messages = ChatMessage.objects.filter(
                room=room
            ).select_related('user').order_by('-timestamp')[:limit]
            
            return [{
                'id': str(msg.id),
                'username': msg.user.username,
                'message': msg.content,
                'timestamp': msg.timestamp.isoformat(),
                'is_system': msg.is_system_message
            } for msg in reversed(messages)]
        except ChatRoom.DoesNotExist:
            return []
    
    @database_sync_to_async
    def save_message(self, content):
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            message = ChatMessage.objects.create(
                room=room,
                user=self.user,
                content=content,
                is_system_message=False
            )
            return {
                'id': str(message.id),
                'timestamp': message.timestamp.isoformat()
            }
        except ChatRoom.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_online_users(self):
        try:
            memberships = RoomMembership.objects.filter(
                room_id=self.room_id,
                is_online=True
            ).select_related('user')
            return [m.user.username for m in memberships]
        except:
            return []
    
    @database_sync_to_async
    def get_all_members(self):
        try:
            memberships = RoomMembership.objects.filter(
                room_id=self.room_id
            ).select_related('user')
            return [m.user.username for m in memberships]
        except:
            return []
