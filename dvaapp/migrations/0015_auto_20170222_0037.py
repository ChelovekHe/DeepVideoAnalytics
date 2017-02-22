# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 00:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dvaapp', '0014_query_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrameLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='frame',
            name='subdir',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='video',
            name='detections',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='framelabel',
            name='frame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dvaapp.Frame'),
        ),
    ]
