# Generated by Django 4.0.3 on 2023-05-19 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0035_alter_project_amount_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='department',
            field=models.SmallIntegerField(choices=[(1, '原前端运维部'), (2, '原网络管理部'), (3, '原传输部'), (4, '原网管中心'), (5, '原安全播出部'), (6, '技术运维部'), (7, '系统技术部'), (8, '前端运行部'), (9, '技术管理部')], verbose_name='负责部门'),
        ),
    ]
