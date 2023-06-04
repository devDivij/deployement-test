# Generated by Django 4.1.7 on 2023-05-17 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randomizer', '0009_imageset_color3_imageset_color4_imageset_color5_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='decision',
            name='categories',
            field=models.ManyToManyField(to='randomizer.category'),
        ),
    ]
