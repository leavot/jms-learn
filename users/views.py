# coding: utf-8

import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from .models import User
from .forms import UserAddForm, UserUpdateForm
from .utils import Bash, ServerUserManager


CONNECTPY_PATH = os.path.join(settings.BASE_DIR, 'init.sh')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def user_add(request):
    form = UserAddForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = form.save(commit=False)
        # user.set_password(password)
        user_in_server = ServerUserManager(Bash)
        ret, msg = user_in_server.present(username=username,
                                          password=password,
                                          shell=CONNECTPY_PATH)
        if not ret:
            user.save()
            return HttpResponseRedirect(reverse('users:list'))
        else:
            user_in_server.absent(username)
            return HttpResponse(msg)
    else:
        error_msg = form.errors
        return HttpResponse('验证失败: %s' % error_msg)


# @login_required装饰器，验证用户已经登陆才可以执行下面的方法，如果没有登陆，跳转到login_url指定的url，
# http://alsww.blog.51cto.com/2001924/1732435
# reverse_lazy用于从urls.py反解url地址，users:login的users是urls.py中的app_name，login是urlpatterns中对应的name，由此得到对应的url地址，如果没有登陆会跳转到此地址
# https://docs.djangoproject.com/en/1.11/ref/urlresolvers/#reverse-lazy
@login_required(login_url=reverse_lazy('users:login'))
# @user_passes_test 装饰器，验证用户是否是管理员，login_url是user_passes_test的可选参数，如果不填默认为settings.LOGIN_URL,lambda定义了一个匿名函数，
@user_passes_test(lambda user: user.is_superuser)
#view里的这个user_update方法接收 request和user_id两个参数
def user_update(request, user_id):
#从model User中获得id为user_id的对象给user,user是model类的一个实例
#http://www.cnpythoner.com/post/105.html
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        #使用instance=user的 modelform UserUpdateFrom实例化form
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            password = form.cleaned_data['password'].strip()
            #save()是modelform的方法，会根据绑定的form表单创建并且保存一个数据库对象，
            #加上commit-False参数会返回一个还未保存至数据库的对象，把表单中传入的password保存到user
            user = form.save(commit=False)
            if password:
                #使用models.User的set_password方法设置密码为password
                user.set_password(password)
                user_in_server = ServerUserManager(Bash)
                ret, msg = user_in_server.present(username=user.username, password=password)
                if ret:
                    return HttpResponse(msg)
            #保存user的内容到数据库
            user.save()
            return HttpResponseRedirect(reverse('users:list'))
#如果不是post方法，就是get方法，从modelform UserUpdateForm取得instance=user的内容给form
    form = UserUpdateForm(instance=user)
#render把{'form': form}的内容加载进users/update.html，并通过浏览器呈现
#http://blog.csdn.net/songyu0219/article/details/52900470?_t_t_t=0.9311686654109508
    return render(request, 'users/update.html', {'form': form})


@login_required(login_url=reverse_lazy('users:login'))
@user_passes_test(lambda user: user.is_superuser)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user/detail.html', {'user': user})


@login_required(login_url=reverse_lazy('users:login'))
@user_passes_test(lambda user: user.is_superuser)
#定义函数用来显示用户列表
def user_list(request):
    #all()方法返回了一个QuerySet，包含database中所有的数据对象。
    #https://www.cnblogs.com/ee2213/p/3914620.html
    users = User.objects.all()
    form = UserAddForm()
    #把users和form的值传入list.html并显示
    return render(request, 'users/list.html', {'users': users, 'form': form})

@login_required(login_url=reverse_lazy('users:login'))
@user_passes_test(lambda user: user.is_superuser)
def user_del(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_in_server = ServerUserManager(Bash)
    ret, msg = user_in_server.absent(user.username, force=True)
    user.delete()
    return HttpResponse('删除成功')

#定义登录函数
def login_(request):
    error = ''
    if request.method == 'POST':
        #在对象request中，POST是django.http.QueryDict的实例，可以取到form中的词典类型数据username和password的值
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        #把上一步取得的的username和passowrd用authentica验证
        user = authenticate(username=username, password=password)
        #如果user不是None，表示用户名密码验证通过
        if user is not None:
            #使用login登录，用户是user
            login(request, user)
            #登录成功后使用HttpResponseRedirect重定向到通过users:list返解得到的地址
            return HttpResponseRedirect(reverse('users:list'))
        else:
            error = '用户密码不正确'
    return render(request, 'users/login.html', {'error': error})


def logout_(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))




