# Generated by Django 3.0.5 on 2020-05-28 07:26

from django.db import migrations
import football_opinionated.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200519_1852'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', football_opinionated.users.models.UserManager()),
            ],
        ),
    ]
