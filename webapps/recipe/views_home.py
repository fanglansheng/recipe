from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.core import serializers
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Q
from recipe.models import *
from recipe.forms import * 
import json

# home that can be accessed by all people even without logging in

def home(request):
    context = {}
    if request.user != None:
        context['work_form'] = CreateWorkForm()
        # context['user_works'] = Work.get_user_work(request.user)
    
    context['all_recipes'] = Recipe.objects.all()
    print("--",request.user)
    return render(request, 'recipe/index.html', context)

@login_required
def get_works(request):
    print("--")
    dic = {}
    maxCount = WorkLog.get_max_id()
    works = Work.objects.filter(Q(deleted=False), 
        Q(user=request.user) | Q(user__profile__following=request.user))\
        .order_by('-date').distinct()
    dic['works'] = [e.as_json() for e in works]
    dic['maxCount'] = maxCount

    data = json.dumps(dic)
    
    return HttpResponse(data, content_type='application/json')


# get the work's photo by work_id
@login_required
def get_work_photo(request, work_id):
    work = get_object_or_404(Work, id=work_id)
    if not work.img:
        print("Cannot find this picture")
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
        print("add_work failed")
        error_str = workForm.errors.as_json()
        error_dict = json.loads(error_str)
        dic['type'] = 'error'
        dic['errors'] = error_dict
        data = json.dumps(dic)
    else:
        print("add_work success")
        work.full_clean()
        work.save()
        workLog = WorkLog(item=work, op='Add')
        workLog.save()
        dic['type'] = 'success'
        dic['new_work'] = work.as_json()
        data = json.dumps(dic)
    # print "save...."
    return HttpResponse(data, content_type='application/json')