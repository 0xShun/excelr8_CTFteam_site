from django.contrib import admin
from .models import Publication, TeamMember, Project
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(Publication, SimpleHistoryAdmin)
admin.site.register(TeamMember, SimpleHistoryAdmin)
admin.site.register(Project, SimpleHistoryAdmin)
