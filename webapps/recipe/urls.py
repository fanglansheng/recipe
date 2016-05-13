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
import recipe.views

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', recipe.views_home.home),
    # works operations:
    url(r'^post_work$', recipe.views_home.add_work, name='add_work'),

	url(r'^home', recipe.views.home, name='hometry'),
    url(r'^login$', recipe.views.loginSelf,  name = 'login'),
	url(r'^logout$', recipe.views.logoutSelf, name = 'logout'),
    url(r'^register$', recipe.views.register,name='register'),
    url(r'^create_recipe$', recipe.views.create_recipe,  name = 'create_recipe'),
	url(r'^get_work_img/(?P<work_id>[0-9]+)$', recipe.views_home.get_work_photo, name='work_img'),
    url(r'^get_all_works$', recipe.views_home.get_works, name='all_works'),
    url(r'^get_work_changes/(?P<maxEntry>\d+)$', recipe.views_home.get_work_changes, name='work_changes'),


]
