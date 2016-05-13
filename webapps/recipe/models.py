from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.core import serializers
import json
from django.forms.models import model_to_dict

# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 100)
    date = models.DateTimeField(auto_now = True)
    bio = models.CharField(max_length = 1000)
    img = models.ImageField(upload_to="recipe",
                            default='recipe/default_recipe.jpg',
                            blank = True)

    def __unicode__(self):
        return self.name

class Step(models.Model):
    recipe = models.ForeignKey(Recipe)
    order = models.IntegerField()               # do we need this?
    text = models.TextField(max_length = 1000)
    img = models.ImageField(upload_to="recipe/step", blank = True)
    def __unicode__(self):
        return self.recipe.name

#???
class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    name = models.CharField(max_length = 100)
    quantity = models.CharField(max_length = 50)
    def __unicode__(self):
        return "%s: %s" % (self.name, self.quantity)
        
class Work(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now = True)
    bio = models.CharField(max_length = 1000, blank=True)
    img = models.ImageField(upload_to="work")
    like = models.ManyToManyField(User,
                            related_name = "liked_work", blank=True)
    recipe = models.ForeignKey(Recipe,
                            related_name = "recipe", blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username

    def as_json(self):
        arr = serializers.serialize('json',[self])
        return arr[1:-1] # get rid of [], because serialize only works for list

    @staticmethod
    def get_user_work(user):        
        return Work.objects.filter(deleted=False,
                    user=user).order_by('-date').distinct()
    @staticmethod
    def get_following_work(user):        
        return Work.objects.filter(deleted=False,
            user__profile__following=user).order_by('-date').distinct()

    # Returns all recent additions and deletions to the work list.
    @staticmethod
    def get_changes(logentry_id=-1):
        return Work.objects.filter(worklog__gt=logentry_id).distinct()

    # Returns all recent additions to the to-do list.
    @staticmethod
    def get_items(logentry_id=-1):
        return Work.objects.filter(deleted=False,
                        worklog__gt=logentry_id).order_by('-date').distinct()
    def delete(self):
        return self.bio

class WorkLog(models.Model):
    item = models.ForeignKey(Work)
    op   = models.CharField(max_length=3, choices=[('Add', 'add'),
                                                   ('Del', 'del')])
    def __unicode__(self):
        return "LogEntry (%d, %s, %s)" % (self.id, self.item, self.op)
    def __str__(self):
        return self.__unicode__()

    # Gets the id of the most recent LogEntry
    @staticmethod
    def get_max_id():
        return WorkLog.objects.all().aggregate(Max('id'))['id__max'] or 0

class Profile(models.Model):
    owner = models.OneToOneField(User, primary_key=True,related_name="profile")
    city = models.CharField(max_length = 20, blank = True)
    country = models.CharField(max_length = 20, blank = True)
    bio = models.CharField(max_length = 420, blank = True)
    img = models.ImageField(upload_to="profile",
                            default='profile/default_user.jpg',
                            blank = True)
    following = models.ManyToManyField(User,
                            related_name = "following", 
                            blank=True)
    saves = models.ManyToManyField(Recipe,
                            related_name = "saves", 
                            blank=True)
    # return a list of user's works
    def get_user_works(self):
        return self.work_set.all()
    def get_user_recipe(self):
        return self.recipe_set.all()

    def __unicode__(self):
        return self.owner.username


# comments for work
class WorkComments(models.Model):
    user = models.ForeignKey(User)
    work = models.ForeignKey(Work)
    content = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now = True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s: %s" % (self.user, self.content)

# comments for recipe
class RecipeComments(models.Model):
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe)
    content = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now = True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s: %s" % (self.user, self.content)