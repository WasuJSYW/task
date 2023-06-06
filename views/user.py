# Create your views here.
import MySQLdb
from django.shortcuts import render, redirect
from task.models import User
from utils.pagination import Pagination
from utils.form import UserModelForm, PasswordResetForm


# 用户页面函数
def user(request):
    queryset = User.objects.all()
    page_object = Pagination(request, queryset, 10)
    return render(request, 'user.html',
                  {'user_list': page_object.page_queryset, 'page_string': page_object.html()})


# 用户表新增处理函数modelform
def user_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'change.html', {"form": form, "title": "新增用户"})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/')
    return render(request, 'change.html', {"form": form, "title": "新增用户"})


# 用户删除处理函数
def user_del(request, nid):
    User.objects.filter(id=nid).delete()
    return redirect('/user/')


# 用户密码重置处理函数modelform
def user_reset(request, nid):
    user = User.objects.filter(id=nid).first()
    title = "密码重置 - {} ".format(user.user_name)
    if request.method == 'GET':
        form = PasswordResetForm(instance=user)
        return render(request, 'change.html', {'form': form, "title": title})
    form = PasswordResetForm(data=request.POST, instance=user)
    if form.is_valid():
        form.save()
        return redirect('/user/')
    return render(request, 'change.html', {'form': form, "title": "编辑用户"})
