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
    context['registerform'] = RegistrationForm()

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

@login_required
def create_recipe(request):
    context={}
    if request.method == 'GET':
        context['recipeForm']=recipeForm(prefix="recipeForm")
        context['stepForm']=stepForm(prefix="stepForm")
        print("get")
        return render(request, 'wanyan/createRecipe.html', context)

    print(request.POST)
    entry = Recipe(user=request.user,date=datetime.now())
    form = recipeForm(request.POST,request.FILES, instance=entry,prefix="recipeForm")

    if not form.is_valid():
        context['stepForm']=stepForm(prefix="stepForm")
        context['recipeForm']=recipeForm(prefix="recipeForm")
        print("recipe not valid")
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
    stepsForm = stepForm(request.POST,request.FILES, instance=step,prefix="stepForm")
    if not stepsForm.is_valid():
        context['recipeForm']=recipeForm(prefix="recipeForm");
        context['stepForm']=stepForm(prefix="stepForm");
        print("step not valid")
        return render(request, 'wanyan/createRecipe.html', context)
   
    # Save the new record
    stepsForm.save()

    return redirect(reverse('hometry'))

@login_required
def recipes(request):
    context={}
    recipes=Recipe.objects.filter(user=request.user)
    context['recipes']=recipes
    return render(request, 'wanyan/recipes.html', context)

@login_required
def get_recipe_photo(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if not recipe.img:
        print("Cannot find this picture")
        raise Http404
    content_type = guess_type(recipe.img.name)
    return HttpResponse(recipe.img, content_type=content_type)

@login_required
def get_step_photo(request, step_id):
    step = get_object_or_404(Recipe, id=step_id)
    if not step.img:
        print("Cannot find this picture")
        raise Http404
    content_type = guess_type(step.img.name)
    return HttpResponse(step.img, content_type=content_type)