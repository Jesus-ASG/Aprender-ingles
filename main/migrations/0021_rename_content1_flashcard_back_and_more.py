# Generated by Django 4.1.2 on 2023-04-29 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_flashcardcollection_user_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flashcard',
            old_name='content1',
            new_name='back',
        ),
        migrations.RenameField(
            model_name='flashcard',
            old_name='content2',
            new_name='front',
        ),
    ]
