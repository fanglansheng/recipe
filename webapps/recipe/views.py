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
from django.contrib.auth import login, authenticate, logout
import json
from datetime import datetime

from recipe.models import *
from recipe.forms import * 

@login_required
def home(request):
    context={};
    return render(request, 'wanyan/home.html', context);
    

@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['registerform'] = RegistrationForm()
        return render(request, 'wanyan/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    registerform = RegistrationForm(request.POST)
    context['registerform'] = registerform

    # Validates the form.
    if not registerform.is_valid():
        return render(request, 'wanyan/login.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=registerform.cleaned_data['username'], 
                                        password=registerform.cleaned_data['password1'],)
    new_user.save()


    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=registerform.cleaned_data['username'],
                            password=registerform.cleaned_data['password1'])
    login(request, new_user)
    context={}
    return redirect(reverse('hometry'))

def loginSelf(request):
    #this is the method to login
    print (User.objects.all())
    context = {}
    context['registerform'] = RegistrationForm()
    if request.method == 'GET':
        return render(request, 'wanyan/login.html', context)

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username = username, password = password)
    print (username, password)

    if user is not None:
        if user.is_active:
           login(request, user)
           return redirect('hometry')
    context['error1'] = "sorry, you are not a merchant"
    return render(request, 'wanyan/login.html', context)

def logoutSelf(request):
    logout(request)
    return redirect('login')

def create_recipe(request):
    context={}
    print(request.POST)
    if request.method=="Get":
        context['recipeForm']=recipeForm()
        context['stepForm']=stepForm()
        return render(request, 'wanyan/createRecipe.html', context)
    
    entry = Recipe(user=request.user,date=datetime.now())
    form = recipeForm(request.POST,request.FILES, instance=entry,prefix="recipeForm")

    if not form.is_valid():
        context['stepForm']=stepForm()
        context['recipeForm']=recipeForm()
        return render(request, 'wanyan/createRecipe.html', context)
   
    # Save the new record
    form.save()

    #not validate
    #for ingredients:
    ingredients=request.POST.getlist('ingname')
    quantities=request.POST.getlist('quantity')
    i=0;
    while i<len(ingredients):
        newIngre=Ingredient(recipe=entry,name=ingredients[i],quantity=quantities[i]);
        newIngre.save();
        i=i+1;
    #steps
    #step = Step(recipe=entry)
    #stepForm = profileform(request.POST, request.FILES, instance=entry)
    step = Step(recipe=entry)
    #stepForm = stepForm(request.POST, request.FILES, instance=step,prefix="stepForm")
    #if not stepForm.is_valid():
    #    context['recipeForm']=recipeForm();
    #    context['stepForm']=stepForm();
    #    return render(request, 'wanyan/createRecipe.html', context)
   
    ## Save the new record
    #stepForm.save()

    return redirect(reverse('hometry'))
