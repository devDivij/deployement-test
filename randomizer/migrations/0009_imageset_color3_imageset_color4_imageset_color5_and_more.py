# Generated by Django 4.1.7 on 2023-04-16 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randomizer', '0008_alter_imageset_color1_alter_imageset_color2'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageset',
            name='color3',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='imageset',
            name='color4',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='imageset',
            name='color5',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='imageset',
            name='color6',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='imageset',
            name='color7',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='imageset',
            name='color8',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='imageset',
            name='color9',
            field=models.CharField(max_length=50, null=True),
        ),
    ]