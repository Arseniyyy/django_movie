# Generated by Django 4.1 on 2023-04-27 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0038_rating_total_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='total_rating',
            field=models.FloatField(default=0),
        ),
    ]