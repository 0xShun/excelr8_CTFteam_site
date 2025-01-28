from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from admin_dashboard.models import TeamMember 

def team_list(request):
    members = TeamMember.objects.all()  # Fetch members from the database
    return render(request, 'team_list.html', {'team_members': members})  # Pass members to the template

def member_detail(request, member_id):
    member = get_object_or_404(TeamMember, pk=member_id)
    return render(request, 'member_detail.html', {'member': member})

def register(request):
    from .models import Member
    from django.shortcuts import redirect

    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        discord = request.POST.get('discord', '')
        facebook = request.POST.get('facebook', '')
        github = request.POST.get('github', '')
        interests = request.POST.getlist('interests')
        other_interest = request.POST.get('other_interest', '')

        # Create a new member object and save it to the database
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

        # Redirect to a success page
        return redirect('registration_success')  # Assuming there's a URL named 'registration_success'

    else:
        # If a GET (or any other method) we'll create a blank form
        return render(request, 'member_registration.html')