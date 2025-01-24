from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('/team_members', views.team_members, name='team_members'),
    path('/publications', views.publications, name='admin_publications'),
    path('/projects', views.projects, name='projects'),
    path('/about_us', views.about_us, name='about_us'),
]
