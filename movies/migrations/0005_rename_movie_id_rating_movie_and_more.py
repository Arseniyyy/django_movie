# Generated by Django 4.1 on 2022-09-12 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_rename_movie_rating_movie_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='movie_id',
            new_name='movie',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='star_id',
            new_name='star',
        ),
    ]
