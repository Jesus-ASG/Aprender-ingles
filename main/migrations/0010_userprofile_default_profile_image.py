# Generated by Django 4.1.2 on 2023-03-18 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_userprofile_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='default_profile_image',
            field=models.CharField(blank=True, choices=[('img/profile_pictures/pp1.jpg', 'Friendly bear'), ('img/profile_pictures/pp2.jpg', 'Thoughtful cat'), ('img/profile_pictures/pp3.jpg', 'Hungry panda')], max_length=50, null=True),
        ),
    ]
