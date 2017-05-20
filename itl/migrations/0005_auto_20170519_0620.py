# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 06:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itl', '0004_auto_20170514_0749'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['playlist_order'],
            },
        ),
        migrations.AlterModelOptions(
            name='kind',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='playlist',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='playlistentry',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itl.Playlist'),
        ),
        migrations.AddField(
            model_name='playlistentry',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itl.Track'),
        ),
    ]
