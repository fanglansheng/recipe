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

from recipe.models import *
from recipe.forms import * 
import json

# home that can be accessed by all people even without logging in
@login_required
def home(request):
    context = {}
    context['work_form'] = CreateWorkForm()
    return render(request, 'recipe/index.html', context)

def add_work(request):
    # work = Work(owner=request.user)
    # workForm = CreateWorkForm(request.POST, instance=work)

    # if not postForm.is_valid():
    #     dic = {}
    #     error_str = postForm.errors.as_json()
    #     error_dict = json.loads(error_str)
    #     dic['type'] = 'error'
    #     dic['content'] = error_dict
    #     data = json.dumps(dic)
    #     return HttpResponse(data, content_type='application/json')
    # # if not 'postContent' in request.POST or not request.POST['postContent']:
    # #     raise Http404
    # else:
    #     new_post.full_clean()
    #     new_post.save()
    #     postLog = PostLog(item=new_post, op='Add')
    #     postLog.save()

    # print "save...."
    return HttpResponse("")