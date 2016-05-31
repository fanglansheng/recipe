from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.core import serializers
from datetime import datetime
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

# home that can be accessed by all people even without logging in
def home(request):
    context = {}
    if request.user != None:
        context['work_form'] = CreateWorkForm()
        # context['user_works'] = Work.get_user_work(request.user)
    
    context['all_recipes'] = Recipe.objects.all()
    return render(request, 'recipe/index.html', context)

@login_required
def get_works(request):
    dic = {}
    maxCount = WorkLog.get_max_id()
    works = Work.get_friends_work(request.user)
    dic['works'] = [e.as_json() for e in works]
    dic['maxCount'] = maxCount
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


# get the work's photo by work_id
@login_required
def get_work_photo(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    if not work.img:
        logger.warning("Cannot find this picture")
        raise Http404
    content_type = guess_type(work.img.name)
    return HttpResponse(work.img, content_type=content_type)

# get work updates (used for ajax)
@login_required
def get_work_changes(request, maxEntry=-1):
    maxCount = WorkLog.get_max_id();
    works = Work.get_changes(maxEntry)
    works = [e.as_json() for e in works]
    dic = {"maxCount" : maxCount, "works": works}
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')

# post new work
@login_required
def add_work(request):
    dic = {}
    # if it is get request then just render the form
    if request.method == "GET":
        dic['work_form'] = CreateWorkForm()
        return HttpResponse(dic)
    # bound data to workform
    work = Work(user=request.user)
    workForm = CreateWorkForm(request.POST, request.FILES, instance=work)
    if not workForm.is_valid():
        logger.warning("add_work failed")
        error_str = workForm.errors.as_json()
        error_dict = json.loads(error_str)
        dic['type'] = 'error'
        dic['errors'] = error_dict
        data = json.dumps(dic)
        logger.debug(data)
    else:
        logger.warning("add_work success")
        work.full_clean()
        work.save()
        workLog = WorkLog(item=work, op='Add')
        workLog.save()
        dic['type'] = 'success'
        dic['new_work'] = work.as_json()
        data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
def delete_work(request, work_id):
    dic = {}
    # Deletes the item if present in the work database.
    try:
        work_to_delete = get_object_or_404(Work, id=work_id)
        if work_to_delete.user == request.user:
            work_to_delete.deleted = True # Just mark items as deleted.
            work_to_delete.save();
            work_log = WorkLog(item=work_to_delete, op='del')
            work_log.save();
            # get comments related to that work
            related_comments = WorkComments.objects.filter(work=work_to_delete)
            for c in related_comments:
                c.delete();
            # work_to_delete.delete()
            dic['type'] = 'success'
            logger.warning("# delete work success!")
        else:
            error = 'Cannot delete wrok that is not belong to you.'
            dic['type'] = 'error'
            dic['errors'] = error
            logger.error(error)
    except ObjectDoesNotExist:
        dic['errors'] = 'The item did not exist in the work list.'
        logger.error(dic['errors'])

    dic['work_id'] = work_id
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


# get all comment of work_id
@login_required
def get_comments_by_work(request, work_id):
    dic = {}
    work = get_object_or_404(Work, id=work_id)
    comments = WorkComments.get_comments(work)
    dic['comments'] = [e.as_json() for e in comments]
    dic['user'] = request.user.username
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


# post new comment
@login_required
def add_comment(request, work_id):
    dic = {}
    towork = get_object_or_404(Work, id=work_id)
    # create a new comment
    comment = WorkComments(user=request.user, work=towork)
    # bound data to commentform
    commentForm = CreateCommentForm(request.POST, instance=comment)
    if not commentForm.is_valid():
        logger.warning("add_comment failed")
        error_str = commentForm.errors.as_json()
        error_dict = json.loads(error_str)
        dic['type'] = 'error'
        dic['errors'] = error_dict
        data = json.dumps(dic)
    else:
        logger.warning("add_comment success")
        comment.save()
        dic['type'] = 'success'
        dic['new_comment'] = comment.as_json()
        data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


@login_required
def delete_work_comment(request, comment_id):
    dic = {}
    comment = get_object_or_404(WorkComments, id=comment_id)
    if comment.user == request.user:
        comment.delete()
        dic['type'] = 'success'
    else:
        dic['type'] = 'error'
        dic['msg'] = 'Cannot delete comment that is not belong to you.'
    dic['comment_id'] = comment_id
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')


def get_all_recipes(request):
    dic = {}
    recipes = Recipe.objects.all()
    # Recipe.objects.all().order_by('saves','headline')
    dic['recipes'] = [e.as_json() for e in recipes]
    data = json.dumps(dic)
    return HttpResponse(data, content_type='application/json')

    