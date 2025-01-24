from django.shortcuts import render, redirect
from .models import TeamMember, Publication, Project
from .forms import TeamMemberForm, PublicationForm, ProjectForm

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def home(request):
    return render(request, 'home.html')

def team_members(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('team_members')
    else:
        form = TeamMemberForm()
    members = TeamMember.objects.all()
    return render(request, 'add_team_members.html', {'team_members': members, 'form': form})

def publications(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('publications') 
    else:
        form = PublicationForm()
    publications_list = Publication.objects.all()
    return render(request, 'add_publications.html', {'publications': publications_list, 'form': form})

def projects(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm()
    projects_list = Project.objects.all()
    return render(request, 'add_projects.html', {'projects': projects_list, 'form': form})