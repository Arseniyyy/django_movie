# Generated by Django 4.1 on 2023-01-09 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0020_actor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user who created this actor'),
        ),
    ]
