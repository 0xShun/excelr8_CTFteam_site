from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'team_management'

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('<int:member_id>/', views.member_detail, name='member_detail'),
    path('register/', views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)