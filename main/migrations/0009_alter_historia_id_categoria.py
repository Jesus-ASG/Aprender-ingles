# Generated by Django 4.1 on 2022-10-06 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_historia_id_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historia',
            name='id_categoria',
            field=models.ManyToManyField(to='main.categoria'),
        ),
    ]
