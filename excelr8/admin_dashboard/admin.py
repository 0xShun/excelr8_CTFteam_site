from django.contrib import admin
from .models import Publication, TeamMember, Project, AboutUs

# Register your models here.
admin.site.register(Publication)
admin.site.register(TeamMember)
admin.site.register(Project)
admin.site.register(AboutUs)
