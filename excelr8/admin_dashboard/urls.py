from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
<<<<<<< HEAD
    path('/team_members', views.team_members, name='team_members'),
    path('/publications', views.publications, name='admin_publications'),
    path('/projects', views.projects, name='projects'),
    path('/about_us', views.about_us, name='about_us'),
=======
    path('add_team_members/', views.team_members, name='add_team_members'),
    path('add_publications/', views.publications, name='add_publications'),
    path('add_projects/', views.projects, name='add_projects'),
>>>>>>> b73a40eb92eadd4b65d51b19149f00ccc5c634c0
]
