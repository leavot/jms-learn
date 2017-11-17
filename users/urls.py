#!/usr/bin/env python
# coding: utf-8
# Created by guang on 
# 


from django.conf.urls import url

from . import views


app_name = 'users'
#urlpatterns中是一组url实例，
urlpatterns = [
    url(r'^$', views.user_list, name='list'),
    url(r'^add/$', views.user_add, name='add'),
#  (?P<name>pattern)中name是组名，pattern是正则规则，这条url中，user_id=符合pattern规则的值  会被作为参数传入 views.user_update
    url(r'^(?P<user_id>[0-9]+)/update/$', views.user_update, name='update'),
    url(r'^(?P<user_id>[0-9]+)/$', views.user_detail, name='detail'),
    url(r'^(?P<user_id>[0-9]+)/del/$', views.user_del, name='del'),
    url(r'^login/$', views.login_, name='login'),
    url(r'^logout/$', views.logout_, name='logout'),
]
