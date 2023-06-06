import json, datetime
from task.models import Inspect
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from utils.pagination import Pagination
from utils.form import LoginForm


def index(request):
    loginform = LoginForm()
    queryset = Inspect.objects.filter()
    page_object = Pagination(request, queryset,50)
    return render(request, 'inspect.html',
                  {'loginform': loginform, 'inspects': page_object.page_queryset, 'page_string': page_object.html})


def QRcode(request):
    code = request.GET.get('code')
    cur_time = datetime.datetime.now()
    if code:
        user = request.session["info"]["name"]
        string = code.split(',')
        if len(string) == 14 and string[1].isalpha() and string[0].isdigit():
            location = string[2] + "U" + string[11]
            name = string[4]
            Inspect.objects.create(user=user, equip=name, location=location, date=cur_time)
            return JsonResponse({"status": True, 'name': name})
        else:
            return JsonResponse({"status": False, 'error': "请扫描设备标签！"})
    return render(request, 'QRcode.html')


def Inspect_delete(request, nid):
    Inspect.objects.filter(id=nid).delete()
    return redirect('/inspect/')
