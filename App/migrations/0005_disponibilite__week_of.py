# Generated by Django 4.0.4 on 2022-08-23 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_remove_disponibilite__week_of'),
    ]

    operations = [
        migrations.AddField(
            model_name='disponibilite',
            name='_week_of',
            field=models.DateField(db_column='week_of', null=True),
        ),
    ]