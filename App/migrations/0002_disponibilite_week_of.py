# Generated by Django 4.0.4 on 2022-08-23 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='disponibilite',
            name='week_of',
            field=models.DateField(null=True),
        ),
    ]