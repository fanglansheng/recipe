from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

# Create your models here.

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
                            blank=True, null=True)
    saves = models.ManyToManyField(Recipe,
                            related_name = "saves", 
                            blank=True, null=True)
    # return a list of user's works
    def get_user_works(self):  
        return self.work_set.all()
    def get_user_recipe(self):
        return self.recipe_set.all()
        
    def __unicode__(self):
        return self.owner.username

class Work(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 100)
    date = models.DateTimeField(auto_now = True)
    bio = models.CharField(max_length = 1000)
    img = models.ImageField(upload_to="recipe", blank = True)
    def __unicode__(self):
        return self.user.username

class Recipe(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 100)
    date = models.DateTimeField(auto_now = True)
    bio = models.CharField(max_length = 1000)
    img = models.ImageField(upload_to="recipe",
                            default='recipe/default_recipe.jpg',
                            blank = True)
    ingredients = models.ManyToManyField(Ingredient, 
                            related_name = "ingredient", 
                            blank=True, null=True)
    steps = models.ManyToManyField(Step,
                            related_name = "step", 
                            blank=True, null=True)
    likes = models.ForeignKey(Work)
    def __unicode__(self):
        return self.work.name

class Step(models.Model):
    recipe = models.ForeignKey(Recipe)
    order = models.IntegerField()               # do we need this?
    text = models.TextField(max_length = 1000)
    img = models.ImageField(upload_to="recipe/step" ,blank = True)


#???
class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    name = models.CharField(max_length = 100)
    quantity = models.CharField(max_length = 50)
    def __unicode__(self):
        return "%s: %s" % (self.name, self.quantity)

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