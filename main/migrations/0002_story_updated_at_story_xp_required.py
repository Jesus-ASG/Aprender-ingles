# Generated by Django 4.1.2 on 2023-02-08 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='story',
            name='xp_required',
            field=models.IntegerField(default=0),
        ),
    ]
