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
