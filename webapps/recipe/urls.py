"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin, auth
import django.contrib.auth.views
import recipe.views_home
import recipe.views_user
import recipe.views

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    # page operation
    url(r'^$', recipe.views_home.home),
    url(r'^profile/(?P<user_id>[0-9]+)$', recipe.views_user.profile),

    # works operations:
    url(r'^post_work$', recipe.views_home.add_work, name='add_work'),
    url(r'^delete_work/(?P<work_id>[0-9]+)$', recipe.views_home.delete_work, name='delete_work'),
    url(r'^get_work_img/(?P<work_id>[0-9]+)$', recipe.views_home.get_work_photo, name='work_img'),
    url(r'^get_all_works$', recipe.views_home.get_works, name='all_works'),
    url(r'^get_work_changes/(?P<maxEntry>\d+)$', recipe.views_home.get_work_changes, name='work_changes'),
    url(r'^like_work/(?P<work_id>[0-9]+)$', recipe.views_home.like_work),
    url(r'^unlike_work/(?P<work_id>[0-9]+)$', recipe.views_home.unlike_work),

    # comments operation:
    url(r'^post_comment/(?P<work_id>[0-9]+)$', recipe.views_home.add_comment, name='add_work_comment'),
    url(r'^delete_work_comment/(?P<comment_id>[0-9]+)$', recipe.views_home.delete_work_comment, name='delete_work_comment'),
    url(r'^get_comments_by_work/(?P<work_id>[0-9]+)$', recipe.views_home.get_comments_by_work),

    # user operation:
    url(r'^get_user_profile/(?P<user_id>[0-9]+)$', recipe.views_user.get_user_profile),
    url(r'^user_photo/(?P<username>\w+)$', recipe.views_user.get_user_image, name='user_img'),
    url(r'^follow/(?P<username>\w+)$', recipe.views_user.follow),
    url(r'^unfollow/(?P<username>\w+)$', recipe.views_user.unfollow),

    # recipe operation:
    url(r'^get_all_recipes$', recipe.views_home.get_all_recipes),

	url(r'^home', recipe.views.home, name='hometry'),
    url(r'^login$', recipe.views.loginSelf,  name = 'login'),
	url(r'^logout$', recipe.views.logoutSelf, name = 'logout'),
    url(r'^register$', recipe.views.register,name='register'),
    url(r'^create_recipe$', recipe.views.create_recipe,  name = 'create_recipe'),
    url(r'^recipes$', recipe.views.recipes,name='recipes'),
    url(r'^get_recipe_img/(?P<recipe_id>[0-9]+)$', recipe.views.get_recipe_photo, name='recipe_img'),
    url(r'^get_step_img/(?P<step_id>[0-9]+)$', recipe.views.get_step_photo, name='step_img'),
    url(r'^delete$', recipe.views.delete, name='delete'),
    url(r'^edit_profile$', recipe.views.edit_profile, name='edit_profile'),
    url(r'^get_user_photo$', recipe.views.get_user_photo, name='get_user_photo'),

]
