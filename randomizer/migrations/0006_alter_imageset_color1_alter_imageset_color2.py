# Generated by Django 4.1.7 on 2023-04-11 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randomizer', '0005_imageset_color1_imageset_color2_alter_imageset_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageset',
            name='color1',
            field=models.CharField(max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='imageset',
            name='color2',
            field=models.CharField(max_length=7, null=True),
        ),
    ]
