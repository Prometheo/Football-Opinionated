# Generated by Django 3.0.5 on 2020-05-02 12:40

import Questions.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=Questions.models.upload_location)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('draft', models.BooleanField()),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'db_table': 'Question_table',
                'ordering': ['created_on'],
            },
        ),
    ]
