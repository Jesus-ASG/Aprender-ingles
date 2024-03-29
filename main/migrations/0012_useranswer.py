# Generated by Django 4.1.2 on 2023-03-24 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('main', '0011_rename_stories_scores_userprofile_scored_stories_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('answer', models.CharField(blank=True, default='', max_length=255)),
                ('submited', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.page')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.story')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='main.userprofile')),
            ],
            options={
                'db_table': 'exercise_answer',
            },
        ),
    ]
