# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('owner', models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('city', models.CharField(max_length=20, blank=True)),
                ('country', models.CharField(max_length=20, blank=True)),
                ('bio', models.CharField(max_length=420, blank=True)),
                ('img', models.ImageField(default=b'profile/default_user.jpg', upload_to=b'profile', blank=True)),
                ('following', models.ManyToManyField(related_name='following', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now=True)),
                ('bio', models.CharField(max_length=1000)),
                ('img', models.ImageField(default=b'recipe/default_recipe.jpg', upload_to=b'recipe', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('recipe', models.ForeignKey(to='recipe.Recipe')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('text', models.TextField(max_length=1000)),
                ('img', models.ImageField(upload_to=b'recipe/step', blank=True)),
                ('recipe', models.ForeignKey(to='recipe.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('bio', models.CharField(max_length=1000)),
                ('img', models.ImageField(upload_to=b'recipe', blank=True)),
                ('like', models.ManyToManyField(related_name='liked_work', to=settings.AUTH_USER_MODEL, blank=True)),
                ('recipe', models.ForeignKey(related_name='recipe', blank=True, to='recipe.Recipe', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('work', models.ForeignKey(to='recipe.Work')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='saves',
            field=models.ManyToManyField(related_name='saves', to='recipe.Recipe', blank=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(to='recipe.Recipe'),
        ),
    ]
