# Generated by Django 4.1 on 2023-01-10 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='owner',
        ),
    ]
