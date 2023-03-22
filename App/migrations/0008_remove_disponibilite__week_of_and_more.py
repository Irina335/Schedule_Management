# Generated by Django 4.0.4 on 2022-08-24 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_alter_schedule__semaine_de'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disponibilite',
            name='_week_of',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='_semaine_de',
        ),
        migrations.AddField(
            model_name='disponibilite',
            name='week_of',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='semaine_de',
            field=models.DateField(default='2022-01-01'),
        ),
    ]
