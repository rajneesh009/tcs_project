# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-07-10 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, upload_to='media', verbose_name='Photo'),
        ),
    ]
