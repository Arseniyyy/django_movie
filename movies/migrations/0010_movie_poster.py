# Generated by Django 4.1 on 2022-12-27 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_remove_movie_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='movies/', verbose_name='Poster'),
        ),
    ]
