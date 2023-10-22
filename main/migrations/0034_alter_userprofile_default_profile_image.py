# Generated by Django 4.2.6 on 2023-10-22 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_storyreport_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='default_profile_image',
            field=models.CharField(blank=True, choices=[('img/profile_pictures/pp1.jpg', 'Friendly bear'), ('img/profile_pictures/pp2.jpg', 'Thoughtful cat'), ('img/profile_pictures/pp3.jpg', 'Hungry panda'), ('img/profile_pictures/pp4.jpg', 'Cute Hamster'), ('img/profile_pictures/pp5.jpg', 'Tall giraffe'), ('img/profile_pictures/pp6.jpg', 'Chilly bird')], max_length=255, null=True),
        ),
    ]
