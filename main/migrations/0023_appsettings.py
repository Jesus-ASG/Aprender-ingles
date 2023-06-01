# Generated by Django 4.1.2 on 2023-06-01 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_flashcardcollection_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'app_settings',
            },
        ),
    ]
