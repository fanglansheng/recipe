from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.core import serializers
from recipe.models import *
from recipe.forms import * 
import json
import logging


# create logger
logger = logging.getLogger('RECIPE')
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('#%(name)s# %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

def profile(request, username):
    context = {}
    context['username'] = username
    return render(request, 'recipe/profile.html', context)

def get_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, owner=user)
    userWorks = Work.get_user_work(user)
    userRecipes = Recipe.get_user_recipes(user)
    fans = Profile.get_fans(profile)

    dic = {}
    dic['profile'] = profile.as_json()
    dic['fans'] = len(fans)
    dic['user_recipes'] = [r.as_json() for r in userRecipes]
    dic['user_works'] = [w.as_json() for w in userWorks]
    data = json.dumps(dic)

    return HttpResponse(data, content_type='application/json')

def get_user_image(request, username):
    user = get_object_or_404(User, username = username)
    profile = get_object_or_404(Profile, owner=user)
    if not profile.img:
        raise Http404
    content_type = guess_type(profile.img.name)
    return HttpResponse(profile.img, content_type=content_type)


@login_required
def unfollow(request, username):
    dic = {}
    try:
        user = User.objects.get(username = request.user)
        follow = User.objects.get(username = username)
        user.profile.following.remove(follow)
        user.save()
        dic['type'] = 'success'
        dic['unfollow'] = follow.username
    except User.DoesNotExist:
        dic['type'] = 'error'
        dic['errors'] = 'This user does not exsit.'
        logger.error(dic['errors'])
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')

@login_required
def follow(request, username):
    dic = {}
    try:
        user = User.objects.get(username = request.user)
        follow = User.objects.get(username = username)
        user.profile.following.add(follow)
        user.save()
        dic['type'] = 'success'
        dic['follow'] = follow.username
    except User.DoesNotExist:
        dic['type'] = 'error'
        dic['errors'] = 'This user does not exsit.'
        logger.error(dic['errors'])
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')