# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-17 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribers', '0002_auto_20180412_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]