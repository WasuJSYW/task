# Generated by Django 4.0.3 on 2022-08-30 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_alter_assets_assets_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='assets',
            name='assets_date',
            field=models.DateField(blank=True, null=True, verbose_name='购置时间'),
        ),
        migrations.AddField(
            model_name='assets',
            name='assets_detail_type',
            field=models.SmallIntegerField(choices=[(3, '监播设备'), (2, 'IP网络设备'), (4, '服务器'), (1, '机房基础设备')], default=1, verbose_name='分项类型'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assets',
            name='assets_total_type',
            field=models.SmallIntegerField(choices=[(1, '硬件'), (3, '其他'), (2, '软件')], default=1, verbose_name='总体类型'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assets',
            name='assets_code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='资产条码'),
        ),
        migrations.AlterField(
            model_name='assets',
            name='assets_room',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='所属机房'),
        ),
        migrations.AlterField(
            model_name='assets',
            name='assets_sn',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='序列号'),
        ),
        migrations.AlterField(
            model_name='assets',
            name='assets_status',
            field=models.SmallIntegerField(choices=[(5, '待入库'), (4, '报废'), (2, '在库'), (3, '维修'), (1, '在线')], verbose_name='当前状态'),
        ),
    ]