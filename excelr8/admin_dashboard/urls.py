from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('add_team_members/', views.team_members, name='add_team_members'),
    path('add_publications/', views.publications, name='add_publications'),
    path('add_projects/', views.projects, name='add_projects'),
    path('edit_team_members/<int:member_id>/', views.edit_team_member, name='edit_team_member'),
    path('edit_publications/<int:publication_id>/', views.edit_publication, name='edit_publication'),
    path('edit_projects/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete_team_members/<int:member_id>/', views.delete_team_member, name='delete_team_member'),
    path('delete_publications/<int:publication_id>/', views.delete_publication, name='delete_publication'),
    path('delete_projects/<int:project_id>/', views.delete_project, name='delete_project'),
    path('member_registration_list/', views.member_registration_list, name='member_registration_list'),
    # Chat management URLs
    path('chat/rooms/', views.chat_rooms, name='chat_rooms'),
    path('chat/rooms/<uuid:room_id>/', views.chat_room_detail, name='chat_room_detail'),
    path('chat/rooms/<uuid:room_id>/delete/', views.delete_chat_room, name='delete_chat_room'),
    path('chat/rooms/<uuid:room_id>/toggle/', views.toggle_chat_room, name='toggle_chat_room'),
    path('chat/rooms/<uuid:room_id>/regenerate/', views.regenerate_invite, name='regenerate_invite'),
    path('chat/users/', views.chat_users, name='chat_users'),
]
