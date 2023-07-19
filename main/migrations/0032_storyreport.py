# Generated by Django 4.1.2 on 2023-07-16 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_audio_description_audio_label_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, default='', max_length=2550)),
                ('status', models.CharField(choices=[('unread', 'Unread'), ('read', 'Read'), ('in_progress', 'In Progress'), ('fixed', 'Fixed')], default='unread', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('fixed_at', models.DateTimeField(null=True)),
                ('page', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='main.page')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='main.story')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userprofile')),
            ],
            options={
                'db_table': 'story_report',
            },
        ),
    ]