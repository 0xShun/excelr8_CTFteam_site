from django.urls import path
from . import views

app_name = 'team_management'

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('<int:member_id>/', views.member_detail, name='member_detail'),
    path('add/', views.add_member, name='add_member'),
    path('edit/<int:member_id>/', views.edit_member, name='edit_member'),
    path('delete/<int:member_id>/', views.delete_member, name='delete_member'),
]
