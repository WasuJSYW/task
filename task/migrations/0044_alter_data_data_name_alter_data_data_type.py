# Generated by Django 4.0.4 on 2023-06-21 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0043_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='data_name',
            field=models.CharField(max_length=100, verbose_name='文档名称'),
        ),
        migrations.AlterField(
            model_name='data',
            name='data_type',
            field=models.SmallIntegerField(choices=[(1, '技术文档'), (2, '演练文档'), (3, '应急预案'), (4, '巡检规范'), (5, '故障处理'), (6, '操作手册')], verbose_name='文档类型'),
        ),
    ]