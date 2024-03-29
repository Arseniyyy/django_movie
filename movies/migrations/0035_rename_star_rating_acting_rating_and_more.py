# Generated by Django 4.1 on 2023-04-27 14:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0034_remove_rating_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='star',
            new_name='acting_rating',
        ),
        migrations.AddField(
            model_name='rating',
            name='cinematography_rating',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddField(
            model_name='rating',
            name='storyline_rating',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
