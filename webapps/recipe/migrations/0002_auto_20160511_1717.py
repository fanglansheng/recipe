# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(blank=True, upload_to='profile', default='profile/default_user.jpg'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='img',
            field=models.ImageField(blank=True, upload_to='recipe', default='recipe/default_recipe.jpg'),
        ),
        migrations.AlterField(
            model_name='step',
            name='img',
            field=models.ImageField(blank=True, upload_to='recipe/step'),
        ),
        migrations.AlterField(
            model_name='work',
            name='img',
            field=models.ImageField(blank=True, upload_to='recipe'),
        ),
    ]
