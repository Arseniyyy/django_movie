# Generated by Django 4.1 on 2022-12-28 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0014_alter_review_text'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RatingStar',
            new_name='Star',
        ),
    ]
