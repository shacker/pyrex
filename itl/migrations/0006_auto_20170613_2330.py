# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-14 06:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itl', '0005_track_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itl.Year'),
        ),
    ]