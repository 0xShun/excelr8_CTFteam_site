# ExcelR8 CTF Team - Terminal Chat Platform

## Overview
A secure, terminal-styled chat platform integrated into the ExcelR8 CTF team website. This platform allows CTF challenge solvers to communicate in real-time chat rooms after solving challenges.

## Features

### Core Features
- ✅ Real-time WebSocket-based chat
- ✅ Terminal-style UI (cyan text on black background)
- ✅ UUID-based room IDs (IDOR protection)
- ✅ Secure password generation
- ✅ User authentication integrated with Django auth
- ✅ Chat-only user accounts (no main site access)
- ✅ Multiple chat rooms support
- ✅ Online/offline user status
- ✅ Message timestamps
- ✅ Message history storage
- ✅ Auto-cleanup of messages older than 1 year

### Chat Commands
- `/help` - Show available commands
- `/users` - List all users in the current room (online/offline)
- `@username` - Mention a user in your message

### Admin Features
- Create and manage chat rooms
- Generate invite links for each room
- View all chat users and their credentials
- Monitor room activity and messages
- Activate/deactivate rooms
- Delete rooms and users
- Regenerate invite links

## Installation & Setup

### Prerequisites
- Python 3.11+
- Virtual environment (recommended)
- Redis (for production) or in-memory channel layer (for development)

### Installation Steps

1. **Install Dependencies**
   ```bash
   cd /home/shun/Documents/arg/excelr8_CTFteam_site
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   cd excelr8
   python manage.py migrate
   ```

3. **Start Redis (Production)**
   ```bash
   sudo systemctl start redis
   # or
   redis-server
   ```
   
   For development without Redis, the in-memory channel layer is already configured in settings.py

4. **Start the Server**
   
   With Daphne (ASGI server for WebSocket support):
   ```bash
   daphne -b 127.0.0.1 -p 8000 excelr8.asgi:application
   ```
   
   Or for development:
   ```bash
   python manage.py runserver
   ```
   Note: `runserver` doesn't support WebSockets in production. Use Daphne for production.

## Usage Guide

### For Administrators

#### 1. Creating a Chat Room
1. Log into the admin dashboard at `/4dm1n_d4shb04rd_3987234098274091823712931/`
2. Click on "Manage Chat Rooms"
3. Enter a room name and click "Create Room"
4. An invite link will be automatically generated

#### 2. Sharing Invite Links
1. Copy the invite link from the chat rooms page
2. Share it as the answer/flag for a CTF challenge
3. Solvers who access the link can sign up and join the chat

#### 3. Managing Users
1. Go to "View Chat Users" from the admin dashboard
2. View all registered chat users
3. See their generated passwords (for password reset requests)
4. Monitor which rooms each user has joined

#### 4. Monitoring Chat Activity
1. Click "View Details" on any room in the chat rooms list
2. See all members, their online status, and recent messages
3. Monitor room activity and engagement

### For CTF Solvers (Chat Users)

#### 1. First-Time Registration
1. Access the invite link provided after solving a challenge
2. Choose a unique username (alphanumeric, underscores, hyphens only)
3. A secure password will be generated for you
4. **IMPORTANT**: Copy and save this password immediately!
5. The password will only be shown once and cannot be reset by users

#### 2. Logging In
1. Visit `/chat/login/`
2. Enter your username and password
3. You'll be redirected to your chat room

#### 3. Using the Chat
1. Type messages in the input box at the bottom
2. Press Enter or Ctrl+Enter to send
3. Use `/help` to see available commands
4. Use `/users` to see who's in the room
5. Mention users with `@username`
6. See online users listed at the top
7. Bookmark the chat room URL for easy access

#### 4. Commands
- `/help` - Display help message
- `/users` - Show all users (online and offline)
- `@username` - Mention a specific user

## URL Structure

### Public URLs
- `/chat/join/<invite-token>/` - Signup page (via invite link)
- `/chat/login/` - Login page for returning users
- `/chat/room/<room-uuid>/` - Chat room (requires authentication)

### Admin URLs
- `/4dm1n_d4shb04rd_3987234098274091823712931/chat/rooms/` - Manage chat rooms
- `/4dm1n_d4shb04rd_3987234098274091823712931/chat/rooms/<room-id>/` - Room details
- `/4dm1n_d4shb04rd_3987234098274091823712931/chat/users/` - View all chat users

## Database Models

### ChatRoom
- `id` (UUID, primary key)
- `name` (CharField)
- `created_at` (DateTimeField)
- `created_by` (ForeignKey to User)
- `is_active` (BooleanField)

### InviteLink
- `token` (UUID, unique)
- `room` (ForeignKey to ChatRoom)
- `created_at` (DateTimeField)
- `is_active` (BooleanField)

### RoomMembership
- `user` (ForeignKey to User)
- `room` (ForeignKey to ChatRoom)
- `joined_at` (DateTimeField)
- `is_online` (BooleanField)
- `last_seen` (DateTimeField)

### ChatMessage
- `id` (UUID, primary key)
- `room` (ForeignKey to ChatRoom)
- `user` (ForeignKey to User)
- `content` (TextField)
- `timestamp` (DateTimeField)
- `is_system_message` (BooleanField)

### ChatUser
- `user` (OneToOneField to User)
- `is_chat_only` (BooleanField)
- `generated_password` (CharField)

## Maintenance Tasks

### Cleanup Old Messages
Messages older than 1 year are automatically eligible for deletion. Run the cleanup command:

```bash
# Dry run (see what would be deleted)
python manage.py cleanup_old_messages --dry-run

# Actually delete old messages
python manage.py cleanup_old_messages
```

### Setting Up Cron Job for Auto-Cleanup
Add to crontab to run monthly:
```bash
0 0 1 * * cd /path/to/project && source venv/bin/activate && python excelr8/manage.py cleanup_old_messages
```

## Production Deployment (PythonAnywhere)

### 1. Update Channel Layers Configuration
Edit `settings.py` to use Redis instead of in-memory:
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

### 2. Install Redis
Follow PythonAnywhere's Redis setup guide or use an external Redis provider.

### 3. Configure ASGI
Set up Daphne as the ASGI server in your PythonAnywhere WSGI configuration file.

### 4. Update ALLOWED_HOSTS
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### 5. Collect Static Files
```bash
python manage.py collectstatic
```

## Security Features

### IDOR Protection
- All room IDs use UUID4 (128-bit random identifiers)
- No sequential or predictable room identifiers
- Membership verification on every WebSocket connection

### Password Security
- Cryptographically secure password generation (16 characters)
- Includes uppercase, lowercase, digits, and special characters
- Passwords stored using Django's built-in password hashing

### Access Control
- Chat users cannot access main site features
- Room membership verified before allowing access
- WebSocket connections authenticated via Django sessions

### Rate Limiting
- Django Axes integration for login attempt monitoring
- Failed login tracking and IP-based blocking

## Troubleshooting

### WebSocket Connection Failed
- Ensure Daphne is running (not Django's runserver in production)
- Check that the WebSocket URL scheme matches (ws:// vs wss://)
- Verify Redis is running if using Redis channel layer

### Users Can't Join Room
- Check that the room is active (`is_active=True`)
- Verify the invite link is active
- Ensure the user has successfully signed up

### Messages Not Appearing
- Check browser console for WebSocket errors
- Verify the user is authenticated
- Ensure the user is a member of the room

### Password Reset Requests
- Only admins can reset passwords
- Access Django admin at `/4dm1n_d4shb04rd_142004/`
- View the generated password in "Chat Users" section
- Or manually reset via Django admin User model

## Browser Compatibility
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

All modern browsers with WebSocket support.

## Sound Effects
- Send message: Subtle click sound
- No sound for receiving messages (to avoid notification spam)

## Future Enhancements
- File sharing in chat
- Private messaging between users
- Chat room themes/customization
- Export chat logs
- User roles (moderators, etc.)
- Message reactions/emojis
- User avatars

## Support
For issues or questions, contact the ExcelR8 CTF team administrators.

---

**Last Updated**: December 6, 2025
**Version**: 1.0.0
