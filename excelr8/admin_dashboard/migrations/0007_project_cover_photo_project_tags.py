# Generated by Django 5.1.2 on 2025-01-25 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0006_alter_publication_authors'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to='project_photos/'),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
