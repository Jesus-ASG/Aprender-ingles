# Generated by Django 4.1.2 on 2023-02-28 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_story_description1_alter_story_description2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='description1',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='story',
            name='description2',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]