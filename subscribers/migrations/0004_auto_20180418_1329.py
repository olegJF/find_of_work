# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-18 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribers', '0003_subscriber_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='password',
            field=models.CharField(default='somepass', max_length=50, verbose_name='Пароль'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Получать рассылку?'),
        ),
    ]
