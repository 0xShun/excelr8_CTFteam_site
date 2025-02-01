from django.shortcuts import render, redirect
from .models import TeamMember, Publication, Project
from .forms import TeamMemberForm, PublicationForm, ProjectForm, EditTeamMemberForm, EditPublicationForm, EditProjectForm
from django.contrib.auth.decorators import user_passes_test
from team_management.models import Member


def superuser_required(view_func):
    return user_passes_test(
        lambda user: user.is_superuser,
        login_url='/4dm1n_d4shb04rd_142004/' 
    )(view_func)

@superuser_required
def admin_dashboard(request):
    team_members = TeamMember.objects.all()
    publications = Publication.objects.all()
    projects = Project.objects.all()
    context = {
        'team_members': team_members,
        'publications': publications,
        'projects': projects
    }
    return render(request, 'admin_dashboard.html', context)

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
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm()
    projects_list = Project.objects.all()
    users_list = TeamMember.objects.all()  # Fetching the list of users
    return render(request, 'add_projects.html', {'projects': projects_list, 'form': form, 'users': users_list})

@superuser_required
def edit_team_member(request, member_id):
    member = TeamMember.objects.get(id=member_id)
    if request.method == 'POST':
        form = EditTeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = EditTeamMemberForm(instance=member)
    return render(request, 'edit_team_member.html', {'form': form})

@superuser_required
def edit_publication(request, publication_id):
    publication = Publication.objects.get(id=publication_id)
    if request.method == 'POST':
        form = EditPublicationForm(request.POST, request.FILES, instance=publication)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = EditPublicationForm(instance=publication)
    return render(request, 'edit_publication.html', {'form': form})

@superuser_required
def edit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = EditProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = EditProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form})

@superuser_required
def delete_team_member(request, member_id):
    TeamMember.objects.get(id=member_id).delete()
    return redirect('admin_dashboard')

@superuser_required
def delete_publication(request, publication_id):
    Publication.objects.get(id=publication_id).delete()
    return redirect('admin_dashboard')

@superuser_required
def delete_project(request, project_id):
    Project.objects.get(id=project_id).delete()
    return redirect('admin_dashboard')

@superuser_required
def member_registration_list(request):
    members = Member.objects.all() 
    return render(request, 'member_registration_list.html', {'members': members})
