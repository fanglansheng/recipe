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
    url(r'^post_work$', recipe.views_home.add_work, name='add_work'),
	# url(r'^home', recipe.views.home, name='hometry'),
	# url(r'^login$', django.contrib.auth.views_home.login, {'template_name':'login.html'},name='login'),
 #    url(r'^logout$', django.contrib.auth.views.logout_then_login ,name='logout'),
    # url(r'^register$', recipe.views.register,name='register'),

	 url(r'^home', recipe.views.home, name='hometry'),
	 #url(r'^login$', django.contrib.auth.views.login, {'template_name':'wanyan/login.html'},name='login'),
  #   url(r'^logout$', django.contrib.auth.views.logout_then_login,name='logout'),
     url(r'^login$', recipe.views.loginSelf,  name = 'login'),
	 url(r'^logout$', recipe.views.logoutSelf, name = 'logout'),
     url(r'^register$', recipe.views.register,name='register'),

]
