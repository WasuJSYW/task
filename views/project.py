import json, datetime, copy
import os

from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import JsonResponse, FileResponse
from task.models import Project, File, Project_File, Assets
from utils.pagination import Pagination
from utils.form import ProjectModelForm, FileModelForm, ProjectfileModelForm, LoginForm
from datetime import timezone
from django.utils.encoding import escape_uri_path
from django.db.models import Sum


@csrf_exempt
def index(request):
    data_dict = {}
    name = request.GET.get('NAME')
    department = request.GET.get('department')
    year = request.GET.get('year')
    form = File.objects.values()
    loginform = LoginForm()
    project_list = []
    schedule_list = []
    key_file_list = []
    deadline_list = []
    cur_time = datetime.date.today()
    cur_date = datetime.datetime.now()
    cur_year = datetime.datetime(year=cur_date.year, month=1, day=1)
    if name:
        data_dict = {"project_name__contains": name}
    if department:
        data_dict = {"department": department}
    if year:
        queryset = Project.objects.filter(Q(**data_dict) & Q(zy_end_date__lte=cur_year)).extra(
            select={"NAME": "inet_aton(project_name)"})
    else:
        queryset = Project.objects.filter(Q(**data_dict) & Q(zy_end_date__gt=cur_year)).extra(
            select={"NAME": "inet_aton(project_name)"})
    for schedule in File.schedule_choices:
        schedule_list.append(schedule[0])
    for project in queryset:
        project_list.append({"project_name": project.project_name})
        key_file = []
        for schedule in schedule_list:
            key_file_queryset = Project_File.objects.filter(
                Q(project_id=project.id) & Q(file__key_file=1) & Q(file__project_schedule=schedule))
            if key_file_queryset.exists():
                for key_file_dict in key_file_queryset.values('file__file_name', 'deadline', 'file_status'):
                    duration = datetime.datetime.strptime(str(key_file_dict['deadline']), '%Y-%m-%d') - cur_date
                    if key_file_dict['deadline'] < cur_time and key_file_dict['file_status'] == '未提交':
                        key_file.append(
                            {'file__file_name': key_file_dict['file__file_name'], 'file_status': 'overtime'})
                    elif key_file_dict['deadline'] >= cur_time and duration.days < 7 and key_file_dict[
                        'file_status'] == '未提交':
                        key_file.append(
                            {'file__file_name': key_file_dict['file__file_name'], 'file_status': 'willovertime'})
                    elif key_file_dict['file_status'] == '已提交':
                        key_file.append(
                            {'file__file_name': key_file_dict['file__file_name'], 'file_status': 'submitted'})
                    else:
                        key_file.append({'file__file_name': key_file_dict['file__file_name'], 'file_status': ''})
            else:
                key_file.append({'file__file_name': ''})
        key_file_list.append(key_file)
        del key_file

        deadline_queryset = Project_File.objects.filter(project_id=project.id).values('project__project_name',
                                                                                      'file__file_name', 'deadline',
                                                                                      'file_status')
        for deadline_dict in deadline_queryset:
            duration = datetime.datetime.strptime(str(deadline_dict['deadline']), '%Y-%m-%d') - cur_date
            if deadline_dict['deadline'] < cur_time and deadline_dict['file_status'] == '未提交':
                deadline_list.append({'project_name': deadline_dict['project__project_name'],
                                      'file_name': deadline_dict['file__file_name'],
                                      'deadline': deadline_dict['deadline'], 'file_status': 'overtime'})
            elif deadline_dict['deadline'] >= cur_time and duration.days < 7 and deadline_dict['file_status'] == '未提交':
                deadline_list.append({'project_name': deadline_dict['project__project_name'],
                                      'file_name': deadline_dict['file__file_name'],
                                      'deadline': deadline_dict['deadline'], 'file_status': 'willovertime'})

        all_price = Assets.objects.filter(project_id=project.id).aggregate(price=Sum('assets_price'))
        if all_price.get("price") is None:
            Project.objects.filter(id=project.id).update(amount_used=0)
        else:
            Project.objects.filter(id=project.id).update(amount_used=all_price['price'])

        projectfile_count = Project_File.objects.filter(project_id=project.id).count()
        if projectfile_count:
            done_count = Project_File.objects.filter(Q(project_id=project.id) & Q(file_status="已提交")).count()
            done_status = '{:.0%}'.format(done_count / projectfile_count)
            Project.objects.filter(id=project.id).update(project_status=done_status)
    if request.POST:
        filequeryset = list(
            File.objects.filter(project_file__project=request.POST['nid']).order_by('project_file__deadline').values(
                'project_file__id', 'project_schedule', 'file_name', 'key_file', 'project_file__file_status',
                'project_file__deadline', 'project_file__submit_time', 'project_file__explain'))
        return JsonResponse(filequeryset, safe=False)
    page_object = Pagination(request, queryset, 10)
    return render(request, 'project.html',
                  {'zip_list': list(zip(project_list, key_file_list)), 'schedule_list': schedule_list,
                   'deadline_list': deadline_list, 'key_file_list': key_file_list, 'form': form, 'loginform': loginform,
                   'projects': page_object.page_queryset, 'page_string': page_object.html()})


def Project_add(request):
    if request.method == 'GET':
        form = ProjectModelForm()
        return render(request, 'change.html', {"form": form, "title": "新增项目"})
    form = ProjectModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/project/')
    return render(request, 'change.html', {"form": form, "title": "新增项目"})


def Project_edit(request, nid):
    project = Project.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = ProjectModelForm(instance=project)
        return render(request, 'change.html', {'form': form, "title": "编辑项目"})
    form = ProjectModelForm(data=request.POST, instance=project)
    if form.is_valid():
        form.save()
        return redirect('/project/')
    return render(request, 'change.html', {'form': form, "title": "编辑项目"})


def Project_delete(request):
    uid = request.GET.get('uid')
    exists = Project.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    Project.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


@csrf_exempt
def File_index(request):
    data_dict = {}
    name = request.GET.get('NAME')
    form = FileModelForm()
    if name:
        data_dict = {"file_name__contains": name}
    queryset = File.objects.filter(**data_dict).extra(select={"NAME": "inet_aton(file_name)"})
    page_object = Pagination(request, queryset, 10)
    return render(request, 'file.html',
                  {'form': form, 'files': page_object.page_queryset, 'page_string': page_object.html()})


def File_add(request):
    if request.method == 'GET':
        form = FileModelForm()
        return render(request, 'change.html', {"form": form, "title": "新增资料"})
    form = FileModelForm(data=request.POST)
    unique = True
    if form.is_valid():
        if request.POST.get('key_file') == '1':
            for file in File.objects.filter(project_schedule=request.POST.get('project_schedule')):
                if file.key_file == 1:
                    unique = False
            if unique:
                form.save()
            else:
                return render(request, 'change.html', {"form": form, "title": "新增资料", "error": "每个阶段只能有一个关键文件"})
        else:
            form.save()
        return redirect('/file/')
    return render(request, 'change.html', {"form": form, "title": "新增资料"})


def File_edit(request, nid):
    file = File.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = FileModelForm(instance=file)
        return render(request, 'change.html', {'form': form, "title": "编辑资料"})
    form = FileModelForm(data=request.POST, instance=file)
    unique = True
    if form.is_valid():
        if request.POST.get('key_file') == '1':
            for file in File.objects.filter(project_schedule=request.POST.get('project_schedule')):
                if file.key_file == 1:
                    unique = False
            if unique:
                form.save()
            else:
                return render(request, 'change.html', {"form": form, "title": "新增资料", "error": "每个阶段只能有一个关键文件"})
        else:
            form.save()
        return redirect('/file/')
    return render(request, 'change.html', {'form': form, "title": "编辑资料"})


def File_delete(request, nid):
    File.objects.filter(id=nid).delete()
    return redirect('/file/')


@csrf_exempt
def projectfile_add(request):
    file_list = request.POST.getlist('check_box_list')
    for file in file_list:
        Project_File.objects.create(file_status="未提交", file_id=file, project_id=request.POST.get('project_id'))
    return JsonResponse({"status": True})


def projectfile_edit(request, nid):
    projectfile = Project_File.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = ProjectfileModelForm(instance=projectfile)
        return render(request, 'change.html', {'form': form, "title": "修改进度"})
    form = ProjectfileModelForm(data=request.POST, instance=projectfile)
    if form.is_valid():
        form.save()
        return redirect('/project/')
    return render(request, 'change.html', {'form': form, "title": "修改进度"})


def projectfile_delete(request):
    uid = request.GET.get('uid')
    exists = Project_File.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    Project_File.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


@csrf_exempt
def projectfile_done(request):
    if request.method == "GET":
        uid = request.GET.get('uid')
        exists = Project_File.objects.filter(id=uid).exists()
        if not exists:
            return JsonResponse({"status": False, 'error': "修改失败，数据不存在"})
        Project_File.objects.filter(id=uid).update(file_status="已提交")
    else:
        uid = request.POST.get('uid')
        exists = Project_File.objects.filter(id=uid).exists()
        if not exists:
            return JsonResponse({"status": False, 'error': "修改失败，数据不存在"})
        Project_File.objects.filter(id=uid).update(file_status="未提交")
    return JsonResponse({"status": True})


def Convert(date):
    time = int(datetime.datetime.combine(date, datetime.time()).replace(tzinfo=timezone.utc).timestamp()) * 1000
    return time


def Project_charts(request):
    nid = request.GET.get('nid')
    if nid:
        project = Project.objects.filter(id=nid).first()
    else:
        project = Project.objects.first()
        nid = project.id
    cur_year = datetime.datetime(year=datetime.datetime.now().year, month=1, day=1)
    depart_project_count = []
    partialFill = []
    data_list = []
    budget_list = []
    difference_budget = [0, 0]
    series_name = project.project_name
    queryset = [{
        "schedule": "需求分析",
        "x": Convert(project.xq_start_date),
        "x2": Convert(project.xq_end_date),
        "y": 0,
    }, {
        "schedule": "项目立项",
        "x": Convert(project.lx_start_date),
        "x2": Convert(project.lx_end_date),
        "y": 1,
    }, {
        "schedule": "项目实施",
        "x": Convert(project.ss_start_date),
        "x2": Convert(project.ss_end_date),
        "y": 2,
    }, {
        "schedule": "项目初验",
        "x": Convert(project.cy_start_date),
        "x2": Convert(project.cy_end_date),
        "y": 3,
    }, {
        "schedule": "项目终验",
        "x": Convert(project.zy_start_date),
        "x2": Convert(project.zy_end_date),
        "y": 4,
    }]
    for project_list in queryset:
        file_count = Project_File.objects.filter(
            Q(project_id=nid) & Q(file__project_schedule__contains=project_list["schedule"])).count()
        done_file_count = Project_File.objects.filter(
            Q(project_id=nid) & Q(file__project_schedule__contains=project_list["schedule"]) & Q(
                file_status="已提交")).count()
        if file_count:
            partialFill.append(done_file_count / file_count)
        else:
            partialFill.append(0)
        data_list.append({
            "x": project_list["x"],
            "x2": project_list["x2"],
            "y": project_list["y"],
            "partialFill": partialFill[project_list["y"]]
        })

    for depart_project in Project.department_choices:
        depart_project_count.append(
            Project.objects.filter(Q(project_depart=depart_project[0]) & Q(cy_end_date__gt=cur_year)).count())

    complete_project_count = [Project.objects.filter(Q(project_status="100%") & Q(cy_end_date__gt=cur_year)).count(),
                              Project.objects.filter(~Q(project_status="100%") & Q(cy_end_date__gt=cur_year)).count()]

    if Project.objects.filter(cy_end_date__gt=cur_year).exists():
        completion_rate = [
            round(int(
                Project.objects.filter(cy_end_date__gt=cur_year).aggregate(rate=Sum('project_status'))['rate']) / int(
                Project.objects.filter(cy_end_date__gt=cur_year).count()), 2)]
        budget_list.append(
            int(Project.objects.filter(cy_end_date__gt=cur_year).aggregate(budget=Sum('project_budget'))['budget']))
        all_amount_used = int(
            Project.objects.filter(cy_end_date__gt=cur_year).aggregate(amount=Sum('amount_used'))['amount'])
        budget_list.append(all_amount_used)
        dif_used = all_amount_used
        for depart in Project.department_choices:
            if Project.objects.filter(Q(project_depart=depart[0]) & Q(cy_end_date__gt=cur_year)).exists():
                depart_amount_used = int(
                    Project.objects.filter(Q(project_depart=depart[0]) & Q(cy_end_date__gt=cur_year)).aggregate(
                        used=Sum('amount_used'))['used'])
                budget_list.append(depart_amount_used)
                dif_used = dif_used - depart_amount_used
                difference_budget.append(dif_used)
            else:
                budget_list.append(0)
                difference_budget.append(0)
    else:
        completion_rate = 0
        budget_list = [0, 0, 0, 0, 0, 0, 0, 0]
        difference_budget = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    result = {
        "status": True,
        "data": {
            'series_name': series_name,
            'data_list': data_list,

            'depart_project_count': depart_project_count,
            'complete_project_count': complete_project_count,

            'completion_rate': completion_rate,

            'budget_list': budget_list,
            'difference_budget': difference_budget,
        }
    }
    return JsonResponse(result)


def Project_upload(request):
    file_id = request.POST.get("projectfile_id")
    if not Project_File.objects.filter(id=file_id).values()[0].get('route') == None:
        path = '.' + Project_File.objects.filter(id=file_id).values()[0].get('route')
        if os.path.exists(path):
            os.remove(path)
    cur_time = datetime.datetime.now().strftime('%Y%m%d')
    file_object = request.FILES.get("avatar")
    if not os.path.exists('./' + cur_time + '/'):
        os.mkdir('./' + cur_time + '/')
    f = open('./' + cur_time + '/' + file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    Project_File.objects.filter(id=file_id).update(route='/' + cur_time + '/' + file_object.name, file_status="已提交",
                                                   submit_time=datetime.datetime.now())
    return redirect('/project/')


def Project_download(request, nid):
    if not Project_File.objects.filter(id=nid).values()[0].get('route') == None:
        path = '.' + Project_File.objects.filter(id=nid).values()[0].get('route')
        file_name = os.path.basename(path)
        if os.path.exists(path):
            response = FileResponse(open(path, 'rb'))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename={0}'.format(escape_uri_path(file_name))
            return response
    return HttpResponse("文件不存在，请上传！")
