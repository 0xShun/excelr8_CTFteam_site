from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('join/<uuid:token>/', views.invite_signup, name='invite_signup'),
    path('login/', views.chat_login, name='login'),
    path('room/<uuid:room_id>/', views.chat_room, name='room'),
]
