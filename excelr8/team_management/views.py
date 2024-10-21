from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

def team_list(request):
    # members = TeamMember.objects.all()
    return render(request, 'team_list.html')

def member_detail(request, member_id):
    member = get_object_or_404(TeamMember, pk=member_id)
    return render(request, 'member_detail.html', {'member': member})

def add_member(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member added successfully.')
            return redirect('team_management:team_list')
    else:
        form = TeamMemberForm()
    return render(request, 'add_member.html', {'form': form})

def edit_member(request, member_id):
    member = get_object_or_404(TeamMember, pk=member_id)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member updated successfully.')
            return redirect('team_management:team_list')
    else:
        form = TeamMemberForm(instance=member)
    return render(request, 'edit_member.html', {'form': form, 'member': member})

def delete_member(request, member_id):
    member = get_object_or_404(TeamMember, pk=member_id)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Team member deleted successfully.')
        return redirect('team_management:team_list')
    return render(request, 'delete_member.html', {'member': member})