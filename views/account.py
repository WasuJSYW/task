from django.shortcuts import render, redirect
from task.models import User
from utils.form import LoginForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = User.objects.filter(**form.cleaned_data).first()
        if not user:
            form.add_error("user_password", "用户名或密码错误")
            return JsonResponse({"status": False, 'error': form.errors})
        request.session["info"] = {'id': user.id, 'name': user.user_name, 'level': user.get_user_level_display()}
        return JsonResponse({"status": True, 'role': request.session["info"]})
    return JsonResponse({"status": False, 'error': form.errors})


def logout(request):
    request.session.clear()
    return JsonResponse({"status": True})
