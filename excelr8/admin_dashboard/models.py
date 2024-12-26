from django.db import models
from django.contrib.auth.models import User  # Importing User model for authors

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Linking Author to User
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username  # Return the username of the linked User

class Publication(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='publications/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)  # Added cover photo field
    created_at = models.DateTimeField(auto_now_add=True)
    authors = models.ManyToManyField('TeamMember', related_name='publications', blank=True)  # Changed to reference TeamMember

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    biography = models.TextField()  # Changed from 'bio' to 'biography' to match the form
    image = models.ImageField(upload_to='team_members/', blank=True, null=True)  # Changed from 'photo' to 'image' to match the form
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.title

class AboutUs(models.Model):
    content = models.TextField()
    mission = models.TextField()
    values = models.TextField()
    team_description = models.TextField()

    def __str__(self):
        return "About Us"
