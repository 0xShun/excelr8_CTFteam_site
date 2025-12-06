# Quick Setup Guide - ExcelR8 CTF Chat Platform

## 🚀 Quick Start (Development)

### 1. Activate Virtual Environment
```bash
cd /home/shun/Documents/arg/excelr8_CTFteam_site
source venv/bin/activate
```

### 2. Start the Server
```bash
cd excelr8
daphne -b 127.0.0.1 -p 8000 excelr8.asgi:application
```

### 3. Access Admin Dashboard
Open browser: `http://127.0.0.1:8000/4dm1n_d4shb04rd_3987234098274091823712931/`

---

## 📋 First-Time Setup (Already Done)

If you need to set up from scratch:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
cd excelr8
python manage.py migrate

# 4. Create superuser (if not exists)
python manage.py createsuperuser

# 5. Start server
daphne -b 127.0.0.1 -p 8000 excelr8.asgi:application
```

---

## 🎯 Testing the Chat Platform

### As Admin:

1. **Login to Admin Dashboard**
   - URL: `http://127.0.0.1:8000/4dm1n_d4shb04rd_3987234098274091823712931/`
   - Use your superuser credentials

2. **Create a Chat Room**
   - Click "Manage Chat Rooms"
   - Enter a room name (e.g., "Test Room")
   - Click "Create Room"
   - Copy the invite link that appears

3. **View Room Details**
   - Click "View Details" on any room
   - See members, messages, and room info

### As User (Testing Signup):

1. **Open Invite Link in Incognito/Private Window**
   - Paste the copied invite link
   - Example: `http://127.0.0.1:8000/chat/join/abc-123-def-456/`

2. **Sign Up**
   - Enter a username (e.g., "testuser")
   - Click "Create Account"
   - **SAVE THE PASSWORD SHOWN!**

3. **Login to Chat**
   - Click "Proceed to Login"
   - Enter username and password
   - You should be redirected to the chat room

4. **Test Chat Features**
   - Send a message
   - Type `/help` to see commands
   - Type `/users` to see user list
   - Try mentioning: `@testuser`
   - Check online users list at top

### As Admin (Multiple Windows):

1. **Open Room in Second Window**
   - Login as different user OR
   - Create second test user
   - Join the same room

2. **Test Real-Time Chat**
   - Send messages from both windows
   - Messages should appear instantly
   - Online user count should update

---

## 🔧 Production Setup (PythonAnywhere)

### 1. Install Redis
```bash
# On PythonAnywhere or your server
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

### 2. Update Settings
Edit `excelr8/excelr8/settings.py`:

```python
# Comment out in-memory layer
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',
#     },
# }

# Uncomment Redis layer
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Update for production
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### 3. Configure ASGI on PythonAnywhere
In your WSGI configuration file, change to use ASGI:

```python
# Use this in your PythonAnywhere web app config
import os
import sys

path = '/home/yourusername/excelr8_CTFteam_site/excelr8'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'excelr8.settings'

from django.core.asgi import get_asgi_application
application = get_asgi_application()
```

---

## 🧪 Testing Checklist

- [ ] Server starts without errors
- [ ] Admin dashboard loads
- [ ] Can create chat room
- [ ] Invite link is generated
- [ ] Can access signup page via invite
- [ ] Password is generated and displayed
- [ ] Can login with credentials
- [ ] Chat room loads
- [ ] WebSocket connects (check browser console)
- [ ] Messages send and receive
- [ ] Online users update
- [ ] `/help` command works
- [ ] `/users` command works
- [ ] @mentions are highlighted
- [ ] Click sound plays on send
- [ ] Second user can join and chat
- [ ] Both users see each other online

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is already in use
lsof -i :8000
# Kill process if needed
kill -9 <PID>
```

### WebSocket connection fails
- Check browser console for errors
- Ensure you're using Daphne (not `runserver`)
- Verify URL scheme (ws:// for HTTP, wss:// for HTTPS)

### Can't access admin dashboard
- Verify you're using the correct URL path
- Check if you're logged in as superuser
- Try clearing browser cache

### Chat messages not appearing
- Check WebSocket connection status in chat room
- Look for errors in browser console
- Verify user is member of the room

### Password not displayed after signup
- Check browser console for JavaScript errors
- Ensure form was submitted successfully
- Try again with different username

---

## 📊 Monitoring Commands

```bash
# Check migrations status
python manage.py showmigrations

# Check database
python manage.py dbshell

# Run cleanup (dry run)
python manage.py cleanup_old_messages --dry-run

# Run cleanup (actual)
python manage.py cleanup_old_messages

# Create superuser
python manage.py createsuperuser
```

---

## 🔐 Admin Access

### Django Admin Panel
- URL: `http://127.0.0.1:8000/4dm1n_d4shb04rd_142004/`
- Manage users, chat rooms, messages directly

### Custom Admin Dashboard
- URL: `http://127.0.0.1:8000/4dm1n_d4shb04rd_3987234098274091823712931/`
- Chat room management
- User overview
- Quick actions

---

## 📱 URLs Reference

### Public URLs
```
/chat/join/<uuid>/        - Signup via invite
/chat/login/              - Chat login
/chat/room/<uuid>/        - Chat room (auth required)
```

### Admin URLs
```
/4dm1n_d4shb04rd_3987234098274091823712931/chat/rooms/                  - Manage rooms
/4dm1n_d4shb04rd_3987234098274091823712931/chat/rooms/<uuid>/          - Room details
/4dm1n_d4shb04rd_3987234098274091823712931/chat/rooms/<uuid>/delete/   - Delete room
/4dm1n_d4shb04rd_3987234098274091823712931/chat/rooms/<uuid>/toggle/   - Toggle active
/4dm1n_d4shb04rd_3987234098274091823712931/chat/rooms/<uuid>/regenerate/ - New invite
/4dm1n_d4shb04rd_3987234098274091823712931/chat/users/                 - View users
```

---

## 💡 Tips

1. **Bookmark Important URLs**
   - Admin dashboard
   - Chat rooms management
   - Django admin

2. **Use Incognito Mode**
   - Test signup flow without logging out
   - Simulate multiple users

3. **Browser Console**
   - F12 or Ctrl+Shift+I
   - Check WebSocket connection
   - Debug JavaScript errors

4. **Save Passwords**
   - Use password manager
   - Store in secure notes
   - Chat users cannot reset their own passwords

5. **Monitor Logs**
   - Terminal output shows server activity
   - Browser console shows client-side issues

---

## 🎉 You're All Set!

The chat platform is now fully functional. Start by:
1. Creating a test room
2. Generating an invite link
3. Testing the signup flow
4. Sending some messages

For detailed documentation, see `CHAT_DOCUMENTATION.md`

---

**Need Help?** Check the implementation summary in `IMPLEMENTATION_SUMMARY.md`
