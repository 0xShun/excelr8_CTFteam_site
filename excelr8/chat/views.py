from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import ChatRoom, InviteLink, RoomMembership, ChatMessage, ChatUser
import secrets
import string
import json


def generate_secure_password(length=16):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Ensure at least one of each type
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]
    # Fill the rest randomly
    password += [secrets.choice(alphabet) for _ in range(length - 4)]
    # Shuffle to avoid predictable pattern
    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    return ''.join(password_list)


@require_http_methods(["GET", "POST"])
def invite_signup(request, token):
    """Signup page for new users via invite link"""
    try:
        invite = get_object_or_404(InviteLink, token=token, is_active=True)
        room = invite.room
        
        if not room.is_active:
            return render(request, 'chat/error.html', {
                'error': 'This chat room is no longer active.'
            })
        
        if request.method == 'POST':
            username = request.POST.get('username', '').strip()
            
            if not username:
                messages.error(request, 'Username is required.')
                return render(request, 'chat/signup.html', {'room': room, 'token': token})
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken. Please choose another.')
                return render(request, 'chat/signup.html', {'room': room, 'token': token})
            
            # Generate secure password
            password = generate_secure_password()
            
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password
            )
            
            # Create chat user profile
            ChatUser.objects.create(
                user=user,
                is_chat_only=True,
                generated_password=password
            )
            
            # Add user to room
            RoomMembership.objects.create(
                user=user,
                room=room
            )
            
            # Show password to user
            return render(request, 'chat/password_display.html', {
                'username': username,
                'password': password,
                'room_id': room.id
            })
        
        return render(request, 'chat/signup.html', {'room': room, 'token': token})
    
    except InviteLink.DoesNotExist:
        return render(request, 'chat/error.html', {
            'error': 'Invalid or expired invite link.'
        })


@require_http_methods(["GET", "POST"])
def chat_login(request):
    """Login page for chat users"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is a chat user
            try:
                chat_profile = user.chat_profile
                if not chat_profile.is_chat_only:
                    messages.error(request, 'Access denied.')
                    return render(request, 'chat/login.html')
            except ChatUser.DoesNotExist:
                messages.error(request, 'Access denied.')
                return render(request, 'chat/login.html')
            
            login(request, user)
            
            # Redirect to room selection or last visited room
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # Get user's first room
            membership = RoomMembership.objects.filter(user=user).first()
            if membership:
                return redirect('chat:room', room_id=membership.room.id)
            
            messages.error(request, 'You are not a member of any chat room.')
            return render(request, 'chat/login.html')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'chat/login.html')


@login_required
def chat_room(request, room_id):
    """Chat room view"""
    # Check if user is a chat-only user
    try:
        chat_profile = request.user.chat_profile
        if not chat_profile.is_chat_only:
            return HttpResponseForbidden("Access denied. This is for chat users only.")
    except ChatUser.DoesNotExist:
        return HttpResponseForbidden("Access denied.")
    
    # Get room and check membership
    room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
    membership = get_object_or_404(RoomMembership, user=request.user, room=room)
    
    # Mark user as online
    membership.is_online = True
    membership.last_seen = timezone.now()
    membership.save()
    
    # Get online users
    online_users = room.get_online_users()
    
    return render(request, 'chat/room.html', {
        'room': room,
        'room_id': str(room.id),
        'online_users': online_users,
        'username': request.user.username
    })


# AJAX API Endpoints

@login_required
@require_GET
def get_messages(request, room_id):
    """API endpoint to fetch messages"""
    try:
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        membership = get_object_or_404(RoomMembership, user=request.user, room=room)
        
        # Update last seen
        membership.last_seen = timezone.now()
        membership.save()
        
        # Get last message ID from request
        last_id = request.GET.get('last_id', 0)
        
        # Fetch new messages
        messages = ChatMessage.objects.filter(
            room=room,
            id__gt=last_id
        ).order_by('timestamp')[:50]
        
        message_list = [{
            'id': msg.id,
            'username': msg.user.username,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat(),
            'is_system': msg.is_system_message
        } for msg in messages]
        
        return JsonResponse({
            'success': True,
            'messages': message_list
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def send_message(request, room_id):
    """API endpoint to send a message"""
    try:
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        membership = get_object_or_404(RoomMembership, user=request.user, room=room)
        
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({'success': False, 'error': 'Empty message'}, status=400)
        
        # Check if it's a command
        if content.startswith('/'):
            response = handle_command(content, request.user, room)
            return JsonResponse({
                'success': True,
                'is_command': True,
                'response': response
            })
        
        # Create message
        message = ChatMessage.objects.create(
            room=room,
            user=request.user,
            content=content
        )
        
        return JsonResponse({
            'success': True,
            'is_command': False,
            'message': {
                'id': message.id,
                'username': message.user.username,
                'content': message.content,
                'timestamp': message.timestamp.isoformat(),
                'is_system': message.is_system_message
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_GET
def get_online_users(request, room_id):
    """API endpoint to get online users"""
    try:
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        membership = get_object_or_404(RoomMembership, user=request.user, room=room)
        
        online_users = room.get_online_users()
        user_list = [{'username': user.username} for user in online_users]
        
        return JsonResponse({
            'success': True,
            'users': user_list,
            'count': len(user_list)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def handle_command(content, user, room):
    """Handle chat commands"""
    parts = content.split()
    command = parts[0].lower()
    
    if command == '/help':
        return """Available commands:
/help - Show this help message
/users - List all users in the room
@username - Mention a user"""
    
    elif command == '/users':
        online_users = room.get_online_users()
        all_members = room.members.all()
        
        online_list = ', '.join([u.username for u in online_users])
        offline_list = ', '.join([m.username for m in all_members if m not in online_users])
        
        response = f"Online ({len(online_users)}): {online_list or 'None'}\n"
        response += f"Offline ({all_members.count() - len(online_users)}): {offline_list or 'None'}"
        return response
    
    else:
        return f"Unknown command: {command}. Type /help for available commands."

