# Generated by Django 4.1 on 2023-04-20 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0030_alter_movie_actors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='star',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Star',
        ),
    ]
