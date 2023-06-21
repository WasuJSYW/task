import json, datetime, os
from task.models import Inspect, Data
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from utils.pagination import Pagination
from utils.form import LoginForm, ProjectModelForm, DataModelForm


def data_index(request):
    loginform = LoginForm()
    queryset = Data.objects.all()
    page_object = Pagination(request, queryset, 50)
    return render(request, 'data.html',
                  {'datas': page_object.page_queryset, 'page_string': page_object.html(), 'loginform': loginform})


def data_add(request):
    if request.method == 'GET':
        form = DataModelForm()
        return render(request, 'dataAdd.html', {"form": form, "title": "新增文档"})
    form = DataModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/data/')
    return render(request, 'dataAdd.html', {"form": form, "title": "新增文档"})


# def data_delete(request, nid):
#     # exists = Data.objects.filter(id=uid).exists()
#     # if not exists:
#     #     return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
#     Data.objects.filter(id=nid).delete()
#     return redirect('/data/')

def data_delete(request):
    uid = request.GET.get('uid')
    exists = Data.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    Data.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def data_edit(request, nid):
    data = Data.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = DataModelForm(instance=data)
        return render(request, 'change.html', {'form': form, "title": "编辑文档"})
    form = DataModelForm(data=request.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/data/')
    return render(request, 'change.html', {'form': form, "title": "编辑文档"})


def data_upload(request):
    data_id = request.POST.get("data_id")
    if not Data.objects.filter(id=data_id).values()[0].get('route') == None:
        path = '.' + Data.objects.filter(id=data_id).values()[0].get('route')
        if os.path.exists(path):
            os.remove(path)
    cur_time = datetime.datetime.now().strftime('%Y%m%d')
    data_object = request.FILES.get("avatar")
    if not os.path.exists('./' + cur_time + '/'):
        os.mkdir('./' + cur_time + '/')
    f = open('./' + cur_time + '/' + data_object.name, mode='wb')
    for chunk in data_object.chunks():
        f.write(chunk)
    f.close()
    Data.objects.filter(id=data_id).update(route='/' + cur_time + '/' + data_object.name, file_status="已提交",
                                           submit_time=datetime.datetime.now())
    return redirect('/data/')
#
#
# def dataFile_download(request, nid):
#     if not Project_File.objects.filter(id=nid).values()[0].get('route') == None:
#         path = '.' + Project_File.objects.filter(id=nid).values()[0].get('route')
#         file_name = os.path.basename(path)
#         if os.path.exists(path):
#             response = FileResponse(open(path, 'rb'))
#             response['content_type'] = "application/octet-stream"
#             response['Content-Disposition'] = 'attachment; filename={0}'.format(escape_uri_path(file_name))
#             return response
#     return HttpResponse("文件不存在，请上传！")
