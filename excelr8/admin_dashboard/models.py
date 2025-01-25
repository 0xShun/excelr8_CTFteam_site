from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username

class Publication(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='publications/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    authors = models.ManyToManyField('TeamMember', related_name='publications', blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    biography = models.TextField()
    image = models.ImageField(upload_to='team_members/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    cover_photo = models.ImageField(upload_to='project_photos/', blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    authors = models.ManyToManyField('TeamMember', related_name='projects', blank=True)  # Allow multiple authors
    history = HistoricalRecords()

    def __str__(self):
        return self.title
        return self.title

class AboutUs(models.Model):
    content = models.TextField()
    mission = models.TextField()
    values = models.TextField()
    team_description = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return "About Us"
