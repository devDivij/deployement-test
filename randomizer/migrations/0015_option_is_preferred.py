# Generated by Django 4.1.7 on 2023-05-20 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randomizer', '0014_decision_situation_delete_situation'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='is_preferred',
            field=models.BooleanField(default=False),
        ),
    ]
