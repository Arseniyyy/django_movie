# Generated by Django 4.1 on 2022-08-23 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(default=None, max_length=5),
        ),
    ]
