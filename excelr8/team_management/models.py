from django.db import models

class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    discord = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    github = models.URLField(blank=True)
    interests = models.JSONField()
    other_interest = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Display name in admin as first name + last name