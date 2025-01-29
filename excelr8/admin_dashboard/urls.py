from django.urls import path
from . import views

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
]
