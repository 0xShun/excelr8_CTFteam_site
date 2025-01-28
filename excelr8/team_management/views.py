from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from admin_dashboard.models import TeamMember 
from .models import Member 
 
def team_list(request):
    members = TeamMember.objects.all()
    return render(request, 'team_list.html', {'team_members': members}) 

def member_detail(request, member_id):
    member = get_object_or_404(TeamMember, pk=member_id)
    return render(request, 'member_detail.html', {'member': member})

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        discord = request.POST.get('discord', '')
        facebook = request.POST.get('facebook', '')
        github = request.POST.get('github', '')
        interests = request.POST.getlist('interests')
        other_interest = request.POST.get('other_interest', '')

        new_member = Member(
            first_name=first_name,
            last_name=last_name,
            email=email,
            discord=discord,
            facebook=facebook,
            github=github,
            interests=interests,
            other_interest=other_interest
        )
        new_member.save()
        messages.success(request, 'Registration successful!') 
        return render(request, 'member_registration.html', {'success': True}) 

    return render(request, 'member_registration.html')