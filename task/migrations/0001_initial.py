# Generated by Django 4.1 on 2022-08-24 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_schedule', models.CharField(choices=[('需求分析', '需求分析'), ('项目立项', '项目立项'), ('项目实施-申购', '项目申购'), ('项目实施-招标', '项目招标'), ('项目实施-入库', '设备入库'), ('项目实施-建设', '项目建设'), ('项目初验', '项目初验'), ('项目终验', '项目终验')], max_length=20, verbose_name='项目阶段')),
                ('file_name', models.CharField(max_length=20, verbose_name='资料名称')),
            ],
        ),
        migrations.CreateModel(
            name='Inspect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20, verbose_name='巡检人员')),
                ('equip', models.CharField(max_length=20, verbose_name='巡检设备')),
                ('location', models.CharField(max_length=20, verbose_name='巡检位置')),
                ('date', models.DateTimeField(verbose_name='巡检时间')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_depart', models.SmallIntegerField(choices=[(1, '前端运维部'), (2, '网络管理部'), (3, '传输部'), (4, '网管中心'), (5, '安全播出部')], verbose_name='负责部门')),
                ('project_name', models.CharField(max_length=20, verbose_name='项目名称')),
                ('project_admin', models.CharField(max_length=32, verbose_name='项目经理')),
                ('project_type', models.SmallIntegerField(choices=[(1, '投资项目'), (2, '客户化项目'), (3, '自主研发项目'), (4, '预算外项目')], verbose_name='项目类型')),
                ('now_schedule', models.CharField(choices=[('需求分析', '需求分析'), ('项目立项', '项目立项'), ('项目实施-申购', '项目实施-申购'), ('项目实施-招标', '项目实施-招标'), ('项目实施-入库', '项目实施-入库'), ('项目实施-建设', '项目实施-建设'), ('项目初验', '项目初验'), ('项目终验', '项目终验')], max_length=20, verbose_name='当前阶段')),
                ('project_budget', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='项目预算')),
                ('amount_used', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='已发生额')),
                ('project_status', models.CharField(default='0%', max_length=32, verbose_name='项目进度')),
                ('xq_start_date', models.DateTimeField(verbose_name='需求分析开始时间')),
                ('xq_end_date', models.DateTimeField(verbose_name='需求分析结束时间')),
                ('lx_start_date', models.DateTimeField(verbose_name='项目立项开始时间')),
                ('lx_end_date', models.DateTimeField(verbose_name='项目立项结束时间')),
                ('ss_start_date', models.DateTimeField(verbose_name='项目实施开始时间')),
                ('ss_end_date', models.DateTimeField(verbose_name='项目实施结束时间')),
                ('cy_start_date', models.DateTimeField(verbose_name='项目初验开始时间')),
                ('cy_end_date', models.DateTimeField(verbose_name='项目初验结束时间')),
                ('zy_start_date', models.DateTimeField(verbose_name='项目终验开始时间')),
                ('zy_end_date', models.DateTimeField(verbose_name='项目终验结束时间')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.SmallIntegerField(choices=[(1, '前端运维部'), (2, '网络管理部'), (3, '传输部'), (4, '网管中心'), (5, '安全播出部')], verbose_name='负责部门')),
                ('task_name', models.CharField(max_length=20, verbose_name='任务名称')),
                ('task_target', models.TextField(max_length=108, verbose_name='任务目标')),
                ('task_admin', models.CharField(max_length=32, verbose_name='负责人')),
                ('task_endline', models.DateTimeField(verbose_name='计划完成时间')),
                ('status', models.CharField(default='0%', max_length=32, verbose_name='任务进度')),
                ('subtask_count', models.IntegerField(null=True, verbose_name='子任务数量')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20, verbose_name='用户名')),
                ('user_password', models.CharField(max_length=32, verbose_name='用户密码')),
                ('user_level', models.SmallIntegerField(choices=[(1, '管理员'), (2, '普通用户')], verbose_name='角色')),
            ],
        ),
        migrations.CreateModel(
            name='Subtask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtask_name', models.CharField(max_length=32, verbose_name='子任务名称')),
                ('subtask_target', models.CharField(max_length=108, verbose_name='子任务目标')),
                ('subtask_endline', models.DateTimeField(verbose_name='计划完成时间')),
                ('subtask_status', models.CharField(choices=[('已完成', '已完成'), ('未完成', '未完成')], max_length=32, verbose_name='完成情况')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task', verbose_name='主任务ID')),
            ],
        ),
        migrations.CreateModel(
            name='Project_File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_status', models.CharField(choices=[('已提交', '已提交'), ('未提交', '未提交')], default='未提交', max_length=20, verbose_name='资料状态')),
                ('deadline', models.DateField(default='2022-01-01', verbose_name='计划提交时间')),
                ('submit_time', models.DateField(blank=True, null=True, verbose_name='实际提交时间')),
                ('explain', models.CharField(blank=True, max_length=20, null=True, verbose_name='备注')),
                ('route', models.CharField(blank=True, max_length=50, null=True, verbose_name='文件路径')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.file', verbose_name='资料ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.project', verbose_name='项目ID')),
            ],
        ),
    ]
