from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('publications/', views.publications, name='publications'),
    path('projects/', views.projects, name='projects'),
    path('register/', views.register, name='register'),
]
