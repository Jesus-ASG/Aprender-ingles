# Generated by Django 4.1.2 on 2023-03-19 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_userprofile_default_profile_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='stories_scores',
            new_name='scored_stories',
        ),
        migrations.AddField(
            model_name='score',
            name='score_percentage',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='default_profile_image',
            field=models.CharField(blank=True, choices=[('/static/img/profile_pictures/pp1.jpg', 'Friendly bear'), ('/static/img/profile_pictures/pp2.jpg', 'Thoughtful cat'), ('/static/img/profile_pictures/pp3.jpg', 'Hungry panda'), ('/static/img/profile_pictures/pp4.jpg', 'Cute Hamster'), ('/static/img/profile_pictures/pp5.jpg', 'Tall giraffe'), ('/static/img/profile_pictures/pp6.jpg', 'Chilly bird')], max_length=50, null=True),
        ),
    ]
