# Generated by Django 4.0.3 on 2022-08-30 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_alter_assets_assets_cabinet_alter_assets_assets_ip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='assets_status',
            field=models.SmallIntegerField(choices=[(5, '待入库'), (3, '维修'), (2, '在库'), (4, '报废'), (1, '在线')], verbose_name='当前状态'),
        ),
    ]
