# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-13 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_auto_20160512_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='img',
            field=models.ImageField(upload_to='work'),
        ),
    ]
