# Generated by Django 4.1 on 2023-04-20 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0027_alter_review_options_alter_actor_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='movies', to='movies.genre', verbose_name='Genres'),
        ),
    ]