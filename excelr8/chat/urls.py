from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # User-facing pages
    path('invite/<uuid:token>/', views.invite_signup, name='invite_signup'),
    path('login/', views.chat_login, name='login'),
    path('room/<uuid:room_id>/', views.chat_room, name='room'),
    
    # AJAX API endpoints
    path('api/<uuid:room_id>/messages/', views.get_messages, name='get_messages'),
    path('api/<uuid:room_id>/send/', views.send_message, name='send_message'),
    path('api/<uuid:room_id>/users/', views.get_online_users, name='get_online_users'),
]
