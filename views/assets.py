from django.shortcuts import render, redirect, HttpResponse
from utils.form import AssetsModelForm, ContractModelForm
from task.models import Assets, Project, Contract
from utils.pagination import Pagination
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Sum


def index(request):
    data_dict = {}
    id = request.GET.get('id')
    name = request.GET.get('NAME')
    page = request.GET.get('page')
    if name:
        data_dict = {"project_id": id, "assets_name__contains": name}
    data_dict = {"project_id": id}
    queryset = Assets.objects.filter(**data_dict).extra(select={"NAME": "inet_aton(assets_name)"})
    for contract in Contract.objects.all():
        all_price = Assets.objects.filter(
            Q(project_id=id) & Q(contract_id=contract.id) & ~Q(assets_status=5)).aggregate(price=Sum('assets_price'))
        Contract.objects.filter(id=contract.id).update(warehouse_price=all_price['price'])
    page_object = Pagination(request, queryset, 10)
    return render(request, 'assets.html',
                  {'project_id': id, 'assets': page_object.page_queryset, 'page_string': page_object.html(),
                   'page': page})


def assets_add(request, nid):
    if request.method == 'GET':
        form = AssetsModelForm(nid)
        return render(request, 'change.html', {"form": form, "title": "新增资产"})
    form = AssetsModelForm(nid,data=request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.project_id = nid
        obj.save()
        return redirect('/assets/?id={}'.format(nid))
    return render(request, 'change.html', {"form": form, "title": "新增资产"})


def assets_edit(request, nid, pid, page):
    assets = Assets.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = AssetsModelForm(pid,instance=assets)
        return render(request, 'change.html', {'form': form, "title": "编辑资产"})
    form = AssetsModelForm(pid,data=request.POST, instance=assets)
    if form.is_valid():
        form.save()
        return redirect('/assets/?id={}&page={}'.format(pid, page))
    return render(request, 'change.html', {'form': form, "title": "编辑资产"})


def assets_delete(request):
    assets_id = request.GET.get('assets_id')
    exists = Assets.objects.filter(id=assets_id).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    Assets.objects.filter(id=assets_id).delete()
    return JsonResponse({"status": True})


def assets_charts(request):
    project_id = request.GET.get('project_id')
    status_count = []
    total_type_count = []
    detail_type_count = []
    total_price = []
    detail_price = []
    assets_date = []
    contract_name = []
    price_name = ['总预算', '已申购额', '成交差额']
    apply_price = Contract.objects.filter(project_id=project_id).aggregate(price=Sum('apply_price'))['price']
    if apply_price:
        apply_price = int(apply_price)
    else:
        apply_price = 0
    all_contract_price = Contract.objects.filter(project_id=project_id).aggregate(price=Sum('contract_price'))['price']
    if all_contract_price:
        all_contract_price = int(all_contract_price)
    else:
        all_contract_price = 0
    all_warehouse_price = Contract.objects.filter(project_id=project_id).aggregate(price=Sum('warehouse_price'))[
        'price']
    if all_warehouse_price:
        all_warehouse_price = int(all_warehouse_price)
    else:
        all_warehouse_price = 0
    price_list = [int(Project.objects.filter(id=project_id).first().project_budget),
                  apply_price,
                  apply_price - all_contract_price,
                  ]
    difference_price = [0, 0, all_contract_price]
    dif_price = all_contract_price
    warehouse_price = [all_warehouse_price, all_warehouse_price, 0]
    unwarehouse_price = [all_contract_price - all_warehouse_price, all_contract_price - all_warehouse_price, 0]
    sum_date_price_list = []
    all_price_list = []

    for status in Assets.status_choices:
        status_count.append(Assets.objects.filter(Q(project_id=project_id) & Q(assets_status=status[0])).count())

    for total_type in Assets.total_type_choices:
        total_type_count.append(
            Assets.objects.filter(Q(project_id=project_id) & Q(assets_total_type=total_type[0])).count())
        all_price = Assets.objects.filter(Q(project_id=project_id) & Q(assets_total_type=total_type[0])).aggregate(
            price=Sum('assets_price'))
        total_price.append(all_price['price'])

    for detail_type in Assets.detail_type_choices:
        detail_type_count.append(
            Assets.objects.filter(Q(project_id=project_id) & Q(assets_detail_type=detail_type[0])).count())
        all_price = Assets.objects.filter(Q(project_id=project_id) & Q(assets_detail_type=detail_type[0])).aggregate(
            price=Sum('assets_price'))
        detail_price.append(all_price['price'])

    for contract in Contract.objects.filter(project_id=project_id):
        contract_name.append((contract.contract_name))
        price_name.append(contract.contract_name)
        price_list.append(int(contract.contract_price))
        dif_price = int(dif_price - contract.contract_price)
        difference_price.append(dif_price)
        warehouse_price.append(contract.warehouse_price)
        if contract.warehouse_price:
            unwarehouse_price.append(contract.contract_price - contract.warehouse_price)
        else:
            unwarehouse_price.append(contract.contract_price - 0)

    for assets in Assets.objects.filter(project=project_id).values('assets_date').distinct().order_by(
            'assets_date'):
        if assets["assets_date"] != None:
            assets_date.append(assets["assets_date"].strftime('%Y-%m-%d'))

    for contract_id in Contract.objects.filter(project_id=project_id):
        date_price_list = []
        for assets in Assets.objects.filter(project=project_id).values('assets_date').distinct().order_by(
                'assets_date'):
            if assets["assets_date"] != None:
                date_price = Assets.objects.filter(
                    Q(project=project_id) & Q(assets_date__lte=assets["assets_date"]) & Q(
                        contract=contract_id.id)).aggregate(price=Sum('assets_price'))['price']
                all_date_price = Assets.objects.filter(Q(project=project_id) & Q(
                    assets_date__lte=assets["assets_date"])).aggregate(price=Sum('assets_price'))['price']
                if date_price == None:
                    date_price_list.append(0)
                else:
                    date_price_list.append(round(int(date_price) / all_contract_price * 100, 2))
                if all_date_price == None:
                    all_price_list.append(0)
                else:
                    all_price_list.append(round(int(all_date_price) / all_contract_price * 100, 2))
        sum_date_price_list.append(date_price_list)
        del date_price_list
    sum_date_price_list.append(all_price_list)

    result = {
        "status": True,
        "data": {
            'status_count': status_count,

            'total_type_count': total_type_count,
            'detail_type_count': detail_type_count,

            'total_price': total_price,
            'detail_price': detail_price,

            'price_name': price_name,
            'price_list': price_list,
            'difference_price': difference_price,
            'warehouse_price': warehouse_price,
            'unwarehouse_price': unwarehouse_price,

            'assets_date': assets_date,
            'sum_date_price_list': sum_date_price_list,
            'contract_name': contract_name,

        }
    }
    return JsonResponse(result)


def contract(request):
    data_dict = {}
    project_id = request.GET.get('project_id')
    name = request.GET.get('NAME')
    form = ContractModelForm()
    if name:
        data_dict = {"project_id": project_id, "contract_name__contains": name}
    else:
        data_dict = {"project_id": project_id}
    queryset = Contract.objects.filter(**data_dict).extra(select={"NAME": "inet_aton(contract_name)"})
    page_object = Pagination(request, queryset, 10)
    return render(request, 'contract.html',
                  {'project_id': project_id, 'form': form, 'contracts': page_object.page_queryset,
                   'page_string': page_object.html()})


def contract_add(request, nid):
    if request.method == 'GET':
        form = ContractModelForm()
        return render(request, 'change.html', {"form": form, "title": "新增合同"})
    form = ContractModelForm(data=request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.project_id = nid
        form.save()
        return redirect('/contract/?project_id={}'.format(nid))
    return render(request, 'change.html', {"form": form, "title": "新增合同"})


def contract_edit(request, nid):
    contract = Contract.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = ContractModelForm(instance=contract)
        return render(request, 'change.html', {'form': form, "title": "编辑合同"})
    form = ContractModelForm(data=request.POST, instance=contract)
    if form.is_valid():
        form.save()
        return redirect('/contract/')
    return render(request, 'change.html', {'form': form, "title": "编辑合同"})


def contract_delete(request):
    contract_id = request.GET.get('contract_id')
    exists = Contract.objects.filter(id=contract_id).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    Contract.objects.filter(id=contract_id).delete()
    return JsonResponse({"status": True})
