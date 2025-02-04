# Generated by Django 5.1.2 on 2024-12-26 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0003_publication_cover_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='publication',
            name='authors',
            field=models.ManyToManyField(blank=True, related_name='publications', to='admin_dashboard.author'),
        ),
    ]
