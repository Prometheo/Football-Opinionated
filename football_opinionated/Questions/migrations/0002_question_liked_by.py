# Generated by Django 3.0.5 on 2020-05-08 08:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
