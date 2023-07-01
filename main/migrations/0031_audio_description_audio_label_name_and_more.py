# Generated by Django 4.1.2 on 2023-07-01 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_alter_image_image_alter_story_cover_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='description',
            field=models.CharField(blank=True, max_length=600),
        ),
        migrations.AddField(
            model_name='audio',
            name='label_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='audio',
            name='show_description',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='audio',
            name='t_description',
            field=models.CharField(blank=True, max_length=600),
        ),
    ]
