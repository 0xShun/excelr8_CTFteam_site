from django import forms
from .models import TeamMember, Publication, Project

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'image', 'biography']  # Added 'biography' for team member details

    def __init__(self, *args, **kwargs):
        super(TeamMemberForm, self).__init__(*args, **kwargs)
        self.fields['biography'].widget.attrs.update({'placeholder': 'Enter a brief biography of the team member.'})

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'description', 'link', 'file']  # Fields for publication details

    def __init__(self, *args, **kwargs):
        super(PublicationForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter the title of the publication.'})

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'link']  # Fields for project details

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter the title of the project.'})

