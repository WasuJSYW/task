import json, datetime, copy

from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import JsonResponse
from task.models import Task, Subtask
from utils.pagination import Pagination
from utils.form import TaskModelForm, SubtaskModelForm, LoginForm


@csrf_exempt
def index(request):
    data_dict = {}
    name = request.GET.get('NAME')
    department = request.GET.get('department')
    month = request.GET.get('month')
    tag = request.GET.get('tag')
    type = request.GET.get('type')
    admin = request.GET.get('admin')
    form = SubtaskModelForm()
    loginform = LoginForm()
    if name:
        data_dict.update({"task_name__contains": name})
    if department:
        data_dict.update({"department": department})
    if tag:
        data_dict.update({"task_tag": tag})
    if type:
        data_dict.update({"task_type": type})
    if month:
        data_dict = {"task_endline__month": month}
    cur_date = datetime.datetime.now().date()
    week = cur_date - datetime.timedelta(weeks=4)
    if request.session.get('info'):
        if request.session.get('info')['level'] == "日常":
            if admin:
                data_dict.update({"task_tag": 3})
                queryset = Task.objects.filter(**data_dict).extra(
                    select={"NAME": "inet_aton(task_name)"}).order_by("task_admin")
            else:
                data_dict.update({"task_tag": 3})
                queryset = Task.objects.filter(**data_dict).extra(
                    select={"NAME": "inet_aton(task_name)"}).order_by("task_endline")
        else:
            if month:
                data_dict = {"task_endline__month": month}
                queryset = Task.objects.filter(**data_dict).extra(
                    select={"NAME": "inet_aton(task_name)"}).order_by("task_endline")
            elif admin:
                queryset = Task.objects.filter(Q(**data_dict) & Q(task_endline__gte=week)).extra(
                    select={"NAME": "inet_aton(task_name)"}).order_by("task_admin")
            else:
                queryset = Task.objects.filter(Q(**data_dict) & Q(task_endline__gte=week)).extra(
                    select={"NAME": "inet_aton(task_name)"}).order_by("task_endline")
    else:
        if month:
            data_dict = {"task_endline__month": month}
            queryset = Task.objects.filter(**data_dict).extra(
                select={"NAME": "inet_aton(task_name)"}).order_by("task_endline")
        elif admin:
            queryset = Task.objects.filter(Q(**data_dict) & Q(task_endline__gte=week)).extra(
                select={"NAME": "inet_aton(task_name)"}).order_by("task_admin")
        else:
            queryset = Task.objects.filter(Q(**data_dict) & Q(task_endline__gte=week)).extra(
                select={"NAME": "inet_aton(task_name)"}).order_by("task_endline")
    for tasks in queryset:
        subtask_count = Subtask.objects.filter(task_id=tasks.id).count()
        if subtask_count:
            subtask_complete_count = Subtask.objects.filter(Q(task_id=tasks.id) & Q(subtask_status="已完成")).count()
            complete_status = '{:.0%}'.format(subtask_complete_count / subtask_count)
            Task.objects.filter(id=tasks.id).update(status=complete_status)
            Task.objects.filter(id=tasks.id).update(subtask_count=subtask_count)
    if request.POST:
        subqueryset = serializers.serialize("json", Subtask.objects.filter(task_id=request.POST['nid']).order_by(
            "subtask_endline"))
        return HttpResponse(subqueryset)
    count = {'task_count': Task.objects.count(), 'subtask_count': Subtask.objects.count(),
             'task_complete_count': Subtask.objects.filter(subtask_status="已完成").count()}
    page_object = Pagination(request, queryset, 10)
    return render(request, 'index.html',
                  {'form': form, 'loginform': loginform, 'count': count, 'tasks': page_object.page_queryset,
                   'page_string': page_object.html()})


def zhuanxiang(request):
    data_dict = {}
    name = request.GET.get('NAME')
    department = request.GET.get('department')
    month = request.GET.get('month')
    data_dict.update({"task_tag": 1})
    type = request.GET.get('type')
    admin = request.GET.get('admin')
    form = SubtaskModelForm()
    loginform = LoginForm()
    if name:
        data_dict.update({"task_name__contains": name})
    if department:
        data_dict.update({"department": department})
    if type:
        data_dict.update({"task_type": type})
    if month:
        data_dict = {"task_endline__month": month}
    cur_date = datetime.datetime.now().date()
    week = cur_date - datetime.timedelta(weeks=4)
    if request.session.get('info'):
        if request.session.get('info')['level'] == "日常":
            if admin:
                data_dict.update({"task_tag": 3})
                queryset = Task.objects.filter(**data_dict).extra(
                    select={"NAME": "inet_aton(task_name)"}).order_by("task_admin")
            else:
                data_dict.update({"task_tag": 3})
                queryset = Task.objects.filter(**data_dict).extra(
                    select={"NAME": "inet_aton(task_name)"}).order_by("task_endline")
        else:
            if month:
                data_dict = {"task_endline__month": month}
                queryset = Task.objects.filter(**data_dict).extra(
                    select={"NAME": "inet_aton(task_name)"}).order_by("task_endline")
            elif admin:
                queryset = Task.objects.filter(Q(**data_dict) & Q(task_endline__gte=week)).extra(
                    select={"NAME": "inet_aton(task_name)"}).order_by("task_admin")
            else:
                queryset = Task.objects.filter(Q(**data_dict) & Q(task_endline__gte=week)).extra(
                    select={"NAME": "inet_aton(task_name)"}).order_by("task_endline")
    else:
        if month:
            data_dict = {"task_endline__month": month}
            queryset = Task.objects.filter(**data_dict).extra(
                select={"NAME": "inet_aton(task_name)"}).order_by("task_endline")
        elif admin:
            queryset = Task.objects.filter(Q(**data_dict) & Q(task_endline__gte=week)).extra(
                select={"NAME": "inet_aton(task_name)"}).order_by("task_admin")
        else:
            queryset = Task.objects.filter(Q(**data_dict) & Q(task_endline__gte=week)).extra(
                select={"NAME": "inet_aton(task_name)"}).order_by("task_endline")
    for tasks in queryset:
        subtask_count = Subtask.objects.filter(task_id=tasks.id).count()
        if subtask_count:
            subtask_complete_count = Subtask.objects.filter(Q(task_id=tasks.id) & Q(subtask_status="已完成")).count()
            complete_status = '{:.0%}'.format(subtask_complete_count / subtask_count)
            Task.objects.filter(id=tasks.id).update(status=complete_status)
            Task.objects.filter(id=tasks.id).update(subtask_count=subtask_count)
    if request.POST:
        subqueryset = serializers.serialize("json", Subtask.objects.filter(task_id=request.POST['nid']).order_by(
            "subtask_endline"))
        return HttpResponse(subqueryset)
    page_object = Pagination(request, queryset, 10)
    return render(request, 'zhuanxiang.html',
                  {'form': form, 'loginform': loginform, 'tasks': page_object.page_queryset,
                   'page_string': page_object.html()})


def Task_add(request):
    if request.method == 'GET':
        form = TaskModelForm()
        return render(request, 'change.html', {"form": form, "title": "新增任务"})
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        if request.POST['task_tag'] == "1":
            return redirect('/zhuanxiang/')
        else:
            return redirect('/index/')
    return render(request, 'change.html', {"form": form, "title": "新增任务"})


def Task_edit(request, nid):
    task = Task.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = TaskModelForm(instance=task)
        return render(request, 'change.html', {'form': form, "title": "编辑任务"})
    form = TaskModelForm(data=request.POST, instance=task)
    if form.is_valid():
        form.save()
        if request.POST['task_tag'] == "1":
            return redirect('/zhuanxiang/')
        else:
            return redirect('/index/')
    return render(request, 'change.html', {'form': form, "title": "编辑任务"})


def Task_delete(request, nid):
    task = Task.objects.filter(id=nid).first()
    Task.objects.filter(id=nid).delete()
    if task.task_tag == 1:
        return redirect('/zhuanxiang/')
    else:
        return redirect('/index/')


@csrf_exempt
def subtask_add(request):
    form = SubtaskModelForm(data=request.POST)
    task_id = request.POST['task_id']
    form.instance.task_id = task_id
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def subtask_delete(request):
    uid = request.GET.get('uid')
    exists = Subtask.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    Subtask.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


@csrf_exempt
def subtask_done(request):
    if request.method == "GET":
        uid = request.GET.get('uid')
        exists = Subtask.objects.filter(id=uid).exists()
        if not exists:
            return JsonResponse({"status": False, 'error': "修改失败，数据不存在"})
        Subtask.objects.filter(id=uid).update(subtask_status="已完成")
    else:
        uid = request.POST.get('uid')
        exists = Subtask.objects.filter(id=uid).exists()
        if not exists:
            return JsonResponse({"status": False, 'error': "修改失败，数据不存在"})
        Subtask.objects.filter(id=uid).update(subtask_status="未完成")
    return JsonResponse({"status": True})


def Task_charts(request):
    data_list = []
    done_subtask = []
    undo_subtask = []
    overdue = []
    for depart in range(1, 6):
        task = []
        done_subtask.append(Subtask.objects.filter(
            Q(subtask_status="已完成") & Q(task__department=depart)).count())
        undo_subtask.append(Subtask.objects.filter(
            Q(subtask_status="未完成") & Q(task__department=depart) & Q(
                subtask_endline__gte=datetime.datetime.now())).count())

        if Subtask.objects.filter(
                Q(subtask_status="未完成") & Q(task__department=depart) & Q(
                    subtask_endline__lt=datetime.datetime.now())).count() > 0:
            overdue.append(Subtask.objects.filter(
                Q(subtask_status="未完成") & Q(task__department=depart) & Q(
                    subtask_endline__lt=datetime.datetime.now())).count())
        else:
            overdue.append('')
        task_stacked_count = 0
        for month in range(1, 13):
            task_count = Task.objects.filter(Q(department=depart) & Q(task_endline__month=month)).count()
            task_stacked_count = task_stacked_count + task_count
            task.append(task_stacked_count)
        data_list.append({
            "department": depart,
            "data_list": task,
        })
        del task
    total_task_count = 0
    task = []
    for month in range(1, 13):
        task_count = Task.objects.filter(task_endline__month=month).count()
        total_task_count = total_task_count + task_count
        task.append(total_task_count)
    data_list.append({
        "department": "总和",
        "data_list": task,
    })
    subtask_list = [Subtask.objects.filter(subtask_status="已完成").count(),
                    Subtask.objects.filter(
                        Q(subtask_status="未完成") & Q(subtask_endline__gte=datetime.datetime.now())).count(),
                    Subtask.objects.filter(
                        Q(subtask_status="未完成") & Q(subtask_endline__lt=datetime.datetime.now())).count()
                    ]
    subtask_schedule = [done_subtask, undo_subtask, overdue]
    subtask_count = []
    for month in range(1, 13):
        subtask_count.append(Subtask.objects.filter(subtask_endline__month=month).count())
    result = {
        "status": True,
        "data": {
            'data_list': data_list,
            'subtask_list': subtask_list,
            'subtask_schedule': subtask_schedule,
            'subtask_count': subtask_count,
        }
    }
    return JsonResponse(result)
