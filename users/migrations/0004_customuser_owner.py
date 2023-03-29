# Generated by Django 4.1 on 2023-01-10 05:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_customuser_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
            preserve_default=False,
        ),
    ]