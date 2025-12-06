from django.shortcuts import render, redirect, get_object_or_404
from .models import TeamMember, Publication, Project
from .forms import TeamMemberForm, PublicationForm, ProjectForm, EditTeamMemberForm, EditPublicationForm, EditProjectForm
from django.contrib.auth.decorators import user_passes_test
from team_management.models import Member
from chat.models import ChatRoom, InviteLink, RoomMembership, ChatMessage, ChatUser
from django.contrib import messages
from django.http import JsonResponse


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


# Chat Management Views
@superuser_required
def chat_rooms(request):
    """View and manage chat rooms"""
    rooms = ChatRoom.objects.all().prefetch_related('memberships', 'invites')
    
    if request.method == 'POST':
        room_name = request.POST.get('room_name', '').strip()
        if room_name:
            # Create room
            room = ChatRoom.objects.create(
                name=room_name,
                created_by=request.user
            )
            # Create invite link
            InviteLink.objects.create(room=room)
            messages.success(request, f'Chat room "{room_name}" created successfully!')
            return redirect('admin_dashboard:chat_rooms')
        else:
            messages.error(request, 'Room name is required.')
    
    # Prepare room data with invite links
    room_data = []
    for room in rooms:
        invite = room.invites.filter(is_active=True).first()
        room_data.append({
            'room': room,
            'invite_token': invite.token if invite else None,
            'member_count': room.memberships.count(),
            'message_count': room.messages.count()
        })
    
    return render(request, 'chat_rooms.html', {'room_data': room_data})


@superuser_required
def chat_room_detail(request, room_id):
    """View details of a specific chat room"""
    room = get_object_or_404(ChatRoom, id=room_id)
    memberships = RoomMembership.objects.filter(room=room).select_related('user')
    messages_list = ChatMessage.objects.filter(room=room).select_related('user').order_by('-timestamp')[:100]
    invite = room.invites.filter(is_active=True).first()
    
    context = {
        'room': room,
        'memberships': memberships,
        'messages': reversed(messages_list),
        'invite_token': invite.token if invite else None,
        'total_messages': room.messages.count()
    }
    
    return render(request, 'chat_room_detail.html', context)


@superuser_required
def delete_chat_room(request, room_id):
    """Delete a chat room"""
    room = get_object_or_404(ChatRoom, id=room_id)
    room_name = room.name
    room.delete()
    messages.success(request, f'Chat room "{room_name}" deleted successfully!')
    return redirect('admin_dashboard:chat_rooms')


@superuser_required
def toggle_chat_room(request, room_id):
    """Activate or deactivate a chat room"""
    room = get_object_or_404(ChatRoom, id=room_id)
    room.is_active = not room.is_active
    room.save()
    status = 'activated' if room.is_active else 'deactivated'
    messages.success(request, f'Chat room "{room.name}" {status}!')
    return redirect('admin_dashboard:chat_rooms')


@superuser_required
def regenerate_invite(request, room_id):
    """Regenerate invite link for a room"""
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # Deactivate old invites
    InviteLink.objects.filter(room=room).update(is_active=False)
    
    # Create new invite
    InviteLink.objects.create(room=room)
    
    messages.success(request, f'New invite link generated for "{room.name}"!')
    return redirect('admin_dashboard:chat_rooms')


@superuser_required
def chat_users(request):
    """View all chat users"""
    chat_users = ChatUser.objects.filter(is_chat_only=True).select_related('user')
    
    users_data = []
    for chat_user in chat_users:
        memberships = RoomMembership.objects.filter(user=chat_user.user).select_related('room')
        users_data.append({
            'chat_user': chat_user,
            'user': chat_user.user,
            'rooms': [m.room for m in memberships],
            'room_count': memberships.count()
        })
    
    return render(request, 'chat_users.html', {'users_data': users_data})
