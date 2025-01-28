from django.shortcuts import render
from admin_dashboard.models import Publication, Project 


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def publications(request):
    publications_list = Publication.objects.prefetch_related('authors').all() 
    return render(request, 'publications.html', {'publications': publications_list})  

def projects(request):
    projects_list = Project.objects.all()  
    return render(request, 'projects.html', {'projects': projects_list})  


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

