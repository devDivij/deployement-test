# Generated by Django 4.1.7 on 2023-05-19 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('randomizer', '0011_situation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='situation',
            name='decision',
        ),
        migrations.AddField(
            model_name='decision',
            name='situation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='decision', to='randomizer.situation'),
        ),
        migrations.AlterField(
            model_name='decision',
            name='categories',
            field=models.ManyToManyField(blank=True, to='randomizer.category'),
        ),
    ]