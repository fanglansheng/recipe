from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.core import serializers
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
import json
from datetime import datetime

from recipe.models import *
from recipe.forms import * 

@login_required
def home(request):
    context={}
    pro=Profile.objects.filter(owner=request.user)
    context={'pro':pro}
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
    
    user = User.objects.get(username = registerform.cleaned_data['username'])
    new_profile=Profile(owner=user)
    new_profile.save()

    login(request, new_user)
    context={}
    return redirect(reverse('hometry'))

def loginSelf(request):
    #this is the method to login
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
    StepFormSet = modelformset_factory(Step, exclude=('recipe',))
    data={
        'form-TOTAL_FORMS': '1',
    }
    if request.method == 'GET':
        context['recipeForm']=recipeForm(prefix="recipeForm")
        context['stepForm']=StepFormSet(prefix="stepForm", queryset=Step.objects.none())
        return render(request, 'wanyan/createRecipe.html', context)

    #print(request.POST)
    entry = Recipe(user=request.user,date=datetime.now())
    form = recipeForm(request.POST,request.FILES, instance=entry,prefix="recipeForm")

    if not form.is_valid():
        context['stepForm']=StepFormSet(prefix="stepForm",queryset=Step.objects.none())
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
    #stepsForm = stepForm(request.POST,request.FILES, instance=step,prefix="stepForm")
    #if not stepsForm.is_valid():
    #    context['recipeForm']=recipeForm(prefix="recipeForm");
    #    context['stepForm']=stepForm(prefix="stepForm");
    #    print("step not valid")
    #    return render(request, 'wanyan/createRecipe.html', context)
   
    # Save the new record
    #stepsForm.save()
    #step = Step(recipe=entry)
    
    step_formset = StepFormSet(request.POST, request.FILES,prefix="stepForm")
    if step_formset.is_valid():
        for step_form in step_formset.forms:
            print(step_form.prefix)
        instances = step_formset.save(commit=False)
        for instance in instances:
            instance.recipe = entry
            #print(instance)
            instance.save()
    else:
        context['stepForm']=StepFormSet(prefix="stepForm",queryset=Step.objects.none())
        context['recipeForm']=recipeForm(prefix="recipeForm")
        print("formset not valid")
        return render(request, 'wanyan/createRecipe.html', context)

    return redirect(reverse('hometry'))

@login_required
def recipes(request):
    context={}
    recipes=Recipe.objects.filter(user=request.user)
    recipeLast=recipes.last()
    aaa = Step.objects.filter()
    context['recipes']=recipes
    for e in aaa.all():
        print(e.text)
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

@login_required
def delete(request):
	#this is the method to cancel an unpaid order
    if request.method == 'GET':
        return redirect('recipes')
    id=request.POST.get('id')
    recipe = Recipe.objects.get(pk = id)
    recipe.delete()
    return redirect(reverse('recipes'))

@login_required
def edit_profile(request):
    profile_to_edit=get_object_or_404(Profile,owner=request.user)
    if request.method == 'GET':
        form=profileForm(instance=profile_to_edit)
        if Profile.objects.filter(owner=request.user).exists():
            context={'form':form}
        else:
            context={'form':form}
        return render(request,'wanyan/editprofile.html',context);

    form=profileForm(request.POST,request.FILES,instance=profile_to_edit)
    if not form.is_valid():
        if Profile.objects.filter(owner=request.user).exists():
            context={'form':form}
        else:
            context={'form':form}
        return render(request,'wanyan/editprofile.html',context);

    form.save()
    return redirect(reverse('hometry'))

@login_required
def get_user_photo(request):
	#this is the method to get a customer's photo
	profile = get_object_or_404(Profile, owner = request.user)
	if not profile.img:
		raise Http404
	content_type = guess_type(profile.img.name)
	return HttpResponse(profile.img, content_type = content_type)