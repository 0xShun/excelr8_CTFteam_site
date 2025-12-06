from django.contrib import admin
from .models import ChatRoom, InviteLink, RoomMembership, ChatMessage, ChatUser


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at', 'created_by', 'is_active', 'get_member_count')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'id')
    readonly_fields = ('id', 'created_at')
    
    def get_member_count(self, obj):
        return obj.get_member_count()
    get_member_count.short_description = 'Members'


@admin.register(InviteLink)
class InviteLinkAdmin(admin.ModelAdmin):
    list_display = ('room', 'token', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('room__name', 'token')
    readonly_fields = ('token', 'created_at')


@admin.register(RoomMembership)
class RoomMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'joined_at', 'is_online', 'last_seen')
    list_filter = ('is_online', 'joined_at', 'room')
    search_fields = ('user__username', 'room__name')
    readonly_fields = ('joined_at',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'content_preview', 'timestamp', 'is_system_message')
    list_filter = ('is_system_message', 'timestamp', 'room')
    search_fields = ('user__username', 'content', 'room__name')
    readonly_fields = ('id', 'timestamp')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_chat_only', 'generated_password')
    list_filter = ('is_chat_only',)
    search_fields = ('user__username',)
