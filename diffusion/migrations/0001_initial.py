# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('msgid', models.CharField(max_length=255)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('headers', models.TextField(null=True, blank=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('msgid', models.CharField(max_length=255)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('headers', models.TextField(null=True, blank=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('closed_at', models.DateTimeField(null=True, blank=True)),
                ('number', models.PositiveIntegerField()),
                ('state', models.CharField(default='open', max_length=10, choices=[('open', 'Open'), ('closed', 'Closed')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
            ],
            options={
                'verbose_name_plural': 'People',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('name', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('description', models.TextField()),
                ('list_id', models.CharField(help_text='List-ID header, as described in RFC2919', unique=True, max_length=255)),
                ('list_email', models.EmailField(help_text='List email address', unique=True, max_length=254)),
                ('web_url', models.CharField(max_length=2000, blank=True)),
                ('scm_url', models.CharField(max_length=2000, blank=True)),
                ('webscm_url', models.CharField(max_length=2000, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patch',
            fields=[
                ('issue_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='diffusion.Issue')),
                ('sha', models.CharField(max_length=255)),
                ('diff', models.TextField()),
                ('version', models.CharField(max_length=16)),
            ],
            options={
                'verbose_name_plural': 'Patches',
            },
            bases=('diffusion.issue',),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('issue_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='diffusion.Issue')),
            ],
            options={
                'verbose_name_plural': 'Series',
            },
            bases=('diffusion.issue',),
        ),
        migrations.AddField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(to='diffusion.Person'),
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(to='diffusion.Project'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to='diffusion.Person'),
        ),
        migrations.AddField(
            model_name='comment',
            name='issue',
            field=models.ForeignKey(to='diffusion.Issue'),
        ),
        migrations.AddField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(to='diffusion.Project'),
        ),
        migrations.AddField(
            model_name='patch',
            name='series',
            field=models.ForeignKey(related_name='patches', to='diffusion.Series'),
        ),
    ]
