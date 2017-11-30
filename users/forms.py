#!/usr/bin/env python
# coding: utf-8
# Created by guang on 
# 


from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from .models import User

#通过modelform，可以实现从model定义一个form类
class   UserAddForm(ModelForm):
    #  通过一个内嵌类 "class Meta" 给 model User定义元数据
    class Meta:
        #model使用User
        model = User
        #fields是要显示的字段
        fields = ['name', 'username', 'password', 'email']
        #widgets用来覆盖fields
        #https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-fields
        widgets = {
            #重新定义字段的类型，placeholder的值Name是填入框的提示文字的内容
            'name': TextInput(attrs={'placeholder': 'Name'}),
            'username': TextInput(attrs={'placeholder': 'username'}),
            'password': PasswordInput(attrs={'placeholder': 'password'}),
            'email': EmailInput(attrs={'placeholder': 'email'})
        }


class UserUpdateForm(ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name','username', 'password', 'email', 'is_superuser', 'is_active']
        widgets = {
            'username': TextInput(attrs={'placeholder': 'username'}),
            'email': EmailInput(attrs={'placeholder': 'email'})
        }
        labels = {
            'is_superuser': 'Is Admin'
        }
