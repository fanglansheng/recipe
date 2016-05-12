from django.shortcuts import render
from recipe.forms import *

# Create your views here.

# home that can be accessed by all people even without logging in
# @login_required
def home(request):
    context = {}
    context['work_form'] = CreateWorkForm()
    return render(request, 'recipe/index.html', context)

def add_work(request):
    context = {}
    context['work_form'] = CreateWorkForm()
    return render(request, 'recipe/index.html', context)