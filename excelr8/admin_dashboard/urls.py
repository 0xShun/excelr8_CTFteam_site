from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('add_team_members/', views.team_members, name='add_team_members'),
    path('add_publications/', views.publications, name='add_publications'),
    path('add_projects/', views.projects, name='add_projects'),
]
