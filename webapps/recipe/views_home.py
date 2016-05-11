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
import json
from datetime import datetime

from recipe.models import *
from recipe.forms import * 

@login_required
def home(request):
	context={};
	return render(request, 'home.html', context);

@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['registerform'] = RegistrationForm()
        return render(request, 'login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    registerform = RegistrationForm(request.POST)
    context['registerform'] = registerform

    # Validates the form.
    if not registerform.is_valid():
        return render(request, 'login.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=registerform.cleaned_data['username'], 
                                        password=registerform.cleaned_data['password1'],)
    new_user.save()


    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=registerform.cleaned_data['username'],
                            password=registerform.cleaned_data['password1'])
    login(request, new_user)
    context={}
    return redirect(reverse('home'))





