from django.shortcuts import render, redirect
from .models import TeamMember, Publication, Project
from .forms import TeamMemberForm, PublicationForm, ProjectForm
from django.contrib.auth.decorators import user_passes_test

def superuser_required(view_func):
    return user_passes_test(
        lambda user: user.is_superuser,
        login_url='/4dm1n_d4shb04rd_142004/' 
    )(view_func)

@superuser_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@superuser_required
def home(request):
    return render(request, 'home.html')

@superuser_required
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

@superuser_required
def publications(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('publications') 
    else:
        form = PublicationForm()
    publications_list = Publication.objects.all()
    users_list = TeamMember.objects.all()  # Fetching the list of users
    return render(request, 'add_publications.html', {'publications': publications_list, 'form': form, 'users': users_list})

@superuser_required
def projects(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm()
    projects_list = Project.objects.all()
    users_list = TeamMember.objects.all()  # Fetching the list of users
    return render(request, 'add_projects.html', {'projects': projects_list, 'form': form, 'users': users_list})