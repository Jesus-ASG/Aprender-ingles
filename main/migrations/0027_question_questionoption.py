# Generated by Django 4.1.2 on 2023-06-08 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_video_delete_videourl'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('element_number', models.IntegerField()),
                ('text', models.CharField(max_length=255)),
                ('t_text', models.CharField(max_length=255)),
                ('randomize_options', models.BooleanField(default=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='main.page')),
            ],
            options={
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('option_number', models.IntegerField(default=0)),
                ('text', models.CharField(max_length=255)),
                ('t_text', models.CharField(max_length=255)),
                ('correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='main.question')),
            ],
            options={
                'db_table': 'question_option',
            },
        ),
    ]
