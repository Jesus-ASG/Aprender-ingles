# Generated by Django 4.1.2 on 2022-10-23 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_historia_ruta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historia',
            name='ruta',
            field=models.CharField(max_length=100, null=True, verbose_name='ruta'),
        ),
    ]
