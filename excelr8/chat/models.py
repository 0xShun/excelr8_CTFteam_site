from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import secrets
import string


class ChatRoom(models.Model):
    """Represents a chat room for CTF challenge solvers"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Name/label for this chat room")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_rooms')
    is_active = models.BooleanField(default=True, help_text="Inactive rooms cannot be accessed")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({str(self.id)[:8]})"
    
    def get_invite_link(self):
        """Get the invite link for this room"""
        invite = self.invites.filter(is_active=True).first()
        if invite:
            return invite.token
        return None
    
    def get_member_count(self):
        """Get the number of members in this room"""
        return self.memberships.count()
    
    def get_online_users(self):
        """Get list of currently online users in this room"""
        return self.memberships.filter(is_online=True).select_related('user')


class InviteLink(models.Model):
    """Invite links for chat rooms - each room has one static invite link"""
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='invites')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invite for {self.room.name}"


class RoomMembership(models.Model):
    """Tracks which users are members of which chat rooms"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_memberships')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='memberships')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'room')
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} in {self.room.name}"


class ChatMessage(models.Model):
    """Individual chat messages"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_system_message = models.BooleanField(default=False, help_text="System messages like join/leave notifications")
    
    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['room', '-timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
    
    @staticmethod
    def generate_secure_password(length=16):
        """Generate a secure random password"""
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password


class ChatUser(models.Model):
    """Extended user profile for chat users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chat_profile')
    is_chat_only = models.BooleanField(default=True, help_text="Users created via invite can only access chat")
    generated_password = models.CharField(max_length=255, blank=True, help_text="Store the initially generated password for admin reference")
    
    def __str__(self):
        return f"ChatProfile: {self.user.username}"
