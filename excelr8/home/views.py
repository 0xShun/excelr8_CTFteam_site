from django.shortcuts import render
from admin_dashboard.models import Publication  # Import the Publication model

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def publications(request):
    publications_list = Publication.objects.all()  # Fetch all publications from the database
    return render(request, 'publications.html', {'publications': publications_list})  # Pass publications to the template
