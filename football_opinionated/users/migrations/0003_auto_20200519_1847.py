# Generated by Django 3.0.5 on 2020-05-19 17:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import football_opinionated.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200519_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=255, verbose_name="user's Bio")),
                ('avatar', models.ImageField(blank=True, default='default.png', upload_to=football_opinionated.users.models.upload_location)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_on', models.DateTimeField(auto_now_add=True)),
                ('current_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='followers', through='users.Friendship', to=settings.AUTH_USER_MODEL),
        ),
    ]
