# Generated by Django 4.1.2 on 2023-04-09 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='text',
        ),
        migrations.AddField(
            model_name='text',
            name='language1',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='text',
            name='language2',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
