from django import forms
from .models import TeamMember, Publication, Project

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'image', 'biography']  # Added 'biography' for team member details

    def __init__(self, *args, **kwargs):
        super(TeamMemberForm, self).__init__(*args, **kwargs)
        self.fields['biography'].widget.attrs.update({'placeholder': 'Enter a brief biography of the team member.'})
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter the full name of the team member.'})
        self.fields['role'].widget.attrs.update({'placeholder': 'Enter the role of the team member.'})
        self.fields['image'].widget.attrs.update({'accept': 'image/*'})

class EditTeamMemberForm(TeamMemberForm):
    class Meta(TeamMemberForm.Meta):
        pass

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'description', 'link', 'file']  # Fields for publication details

    def __init__(self, *args, **kwargs):
        super(PublicationForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter the title of the publication.'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Enter a brief description of the publication.'})
        self.fields['link'].widget.attrs.update({'placeholder': 'Enter the link to the publication.'})
        self.fields['file'].widget.attrs.update({'accept': 'application/pdf'})

class EditPublicationForm(PublicationForm):
    class Meta(PublicationForm.Meta):
        pass

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'link', 'cover_photo', 'tags', 'authors']  # Updated fields for project details

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter the title of the project.'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Enter a detailed description of the project.'})
        self.fields['link'].widget.attrs.update({'placeholder': 'Enter the link to the project.'})
        self.fields['cover_photo'].widget.attrs.update({'accept': 'image/*'})
        self.fields['tags'].widget.attrs.update({'placeholder': 'Enter comma-separated tags.'})
        self.fields['authors'].widget.attrs.update({'placeholder': 'Select authors related to the project.'})

class EditProjectForm(ProjectForm):
    class Meta(ProjectForm.Meta):
        pass
