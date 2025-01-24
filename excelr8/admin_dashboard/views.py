from django.shortcuts import render, redirect
from .models import TeamMember, Publication, Project
from .forms import TeamMemberForm, PublicationForm, ProjectForm

# Create your views here.
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def home(request):
    return render(request, 'home.html')

def team_members(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if form.is_valid():
            form.save()  # Save the new team member to the database
            return redirect('team_members')  # Redirect to the team members page
    else:
        form = TeamMemberForm()
    members = TeamMember.objects.all()  # Fetch all team members from the database
    return render(request, 'team_members.html', {'team_members': members, 'form': form})


def publications(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES)  # Include request.FILES for file upload
        if form.is_valid():
            form.save()  # Save the new publication to the database
            return redirect('publications')  # Redirect to the publications page
    else:
        form = PublicationForm()
    publications_list = Publication.objects.all()  # Fetch all publications from the database
    return render(request, 'publications.html', {'publications': publications_list, 'form': form})

def projects(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)  # No file upload for projects
        if form.is_valid():
            form.save()  # Save the new project to the database
            return redirect('projects')  # Redirect to the projects page
    else:
        form = ProjectForm()
    projects_list = Project.objects.all()  # Fetch all projects from the database
    return render(request, 'projects.html', {'projects': projects_list, 'form': form})

def about_us(request):
    return render(request, 'aboutus.html')
