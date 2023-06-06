"""tms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from views import task, project, inspect, user, account, assets

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', task.index),
    path('zhuanxiang/', task.zhuanxiang),

    path('task/add/', task.Task_add),
    path('task/<int:nid>/delete/', task.Task_delete),
    path('task/<int:nid>/edit/', task.Task_edit),
    path('task/charts/', task.Task_charts),

    path('subtask/add/', task.subtask_add),
    path('subtask/delete/', task.subtask_delete),
    path('subtask/done/', task.subtask_done),

    path('project/', project.index),
    path('project/add/', project.Project_add),
    path('project/<int:nid>/edit/', project.Project_edit),
    path('project/delete/', project.Project_delete),
    path('project/charts/', project.Project_charts),
    path('project/upload/', project.Project_upload),
    path('project/<int:nid>/download/', project.Project_download),

    path('file/', project.File_index),
    path('file/add/', project.File_add),
    path('file/<int:nid>/edit/', project.File_edit),
    path('file/<int:nid>/delete/', project.File_delete),

    path('projectfile/add/', project.projectfile_add),
    path('projectfile/delete/', project.projectfile_delete),
    path('projectfile/<int:nid>/edit/', project.projectfile_edit),
    path('projectfile/done/', project.projectfile_done),

    path('inspect/', inspect.index),
    path('inspect/QRcode/', inspect.QRcode),
    path('inspect/<int:nid>/delete/', inspect.Inspect_delete),

    path('user/', user.user),
    path('user/add/', user.user_add),
    path('user/<int:nid>/delete/', user.user_del),
    path('user/<int:nid>/reset/', user.user_reset),

    path('account/', account.login),
    path('logout/', account.logout),

    path('assets/', assets.index),
    path('assets/<int:nid>/add/', assets.assets_add),
    path('assets/<int:nid>/<int:pid>/<int:page>/edit/', assets.assets_edit),
    path('assets/delete/', assets.assets_delete),
    path('assets/charts/', assets.assets_charts),

    path('contract/', assets.contract),
    path('contract/<int:nid>/add/', assets.contract_add),
    path('contract/<int:nid>/edit/', assets.contract_edit),
    path('contract/delete/', assets.contract_delete),
]
