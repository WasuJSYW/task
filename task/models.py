from django.db import models


# Create your models here.
class Task(models.Model):
    department_choices = (
        (1, "原前端运维部"),
        (2, "原网络管理部"),
        (3, "原传输部"),
        (4, "原网管中心"),
        (5, "原安全播出部"),
        (6, "前端运维中心"),
        (7, "系统技术部"),
        (8, "前端运行部"),
        (9, "技术管理部"),
        (10, "平台技术中心"),
        (11, "基础运维中心"),
        (12, "信息技术中心"),
        (13, "前端运维中心/基础运维中心"),
        (14, "技术运维部"),
        (15, "直播监测部"),
        (16, "运行管理部"),
        (17, "分前端管理部"),
        (18, "区县前端管理部"),
    )
    tag_choices = (
        (1, "亚运任务"),
        (2, "二十大任务"),
        (3, "日常任务"),
    )
    type_choices = (
        (1, "工作会议"),
        (2, "预案更新"),
        (3, "检测维护"),
        (4, "演练"),
        (5, "培训考核"),
        (6, "亚运建设"),
        (7, "资产管理"),
        (8, "系统/项目建设"),
        (9, "文档修订"),
        (10, "图纸更新"),
        (20, "其他"),
    )
    department = models.SmallIntegerField(verbose_name="负责部门", choices=department_choices)
    task_name = models.CharField(verbose_name="任务名称", max_length=64)
    task_tag = models.SmallIntegerField(verbose_name="任务标签", choices=tag_choices)
    task_type = models.SmallIntegerField(verbose_name="任务类型", choices=type_choices)
    task_target = models.TextField(verbose_name="任务目标", max_length=256)
    task_admin = models.CharField(verbose_name="负责人", max_length=32)
    task_endline = models.DateTimeField(verbose_name="计划完成时间")
    status = models.CharField(verbose_name="任务进度", max_length=32, default="0%")
    subtask_count = models.IntegerField(verbose_name="子任务数量", null=True)


class Subtask(models.Model):
    subtask_name = models.CharField(verbose_name="子任务名称", max_length=32)
    subtask_target = models.CharField(verbose_name="子任务目标", max_length=108)
    subtask_endline = models.DateTimeField(verbose_name="计划完成时间")
    subtask_status_choices = (
        ("已完成", "已完成"),
        ("未完成", "未完成"),
    )
    subtask_status = models.CharField(verbose_name="完成情况", max_length=32, choices=subtask_status_choices)
    task = models.ForeignKey(verbose_name="主任务ID", to="Task", to_field="id", on_delete=models.CASCADE)


class Project(models.Model):
    department_choices = (
        (1, "前端运维部"),
        (2, "网络管理部"),
        (3, "传输部"),
        (4, "网管中心"),
        (5, "安全播出部"),
        (6, "技术运维部"),
    )
    type_choices = (
        (1, "投资项目"),
        (2, "客户化项目"),
        (3, "自主研发项目"),
        (4, "预算外项目"),
    )
    project_depart = models.SmallIntegerField(verbose_name="负责部门", choices=department_choices)
    project_name = models.CharField(verbose_name="项目名称", max_length=20)
    project_admin = models.CharField(verbose_name="项目经理", max_length=32)
    project_type = models.SmallIntegerField(verbose_name="项目类型", choices=type_choices)
    project_budget = models.DecimalField(verbose_name="项目预算", max_digits=10, decimal_places=2)
    amount_used = models.DecimalField(verbose_name="已发生额", max_digits=10, decimal_places=2, default=0)
    project_status = models.CharField(verbose_name="项目进度", max_length=32, default="0%")
    xq_start_date = models.DateField(verbose_name="需求分析开始时间")
    xq_end_date = models.DateField(verbose_name="需求分析结束时间")
    lx_start_date = models.DateField(verbose_name="项目立项开始时间")
    lx_end_date = models.DateField(verbose_name="项目立项结束时间")
    ss_start_date = models.DateField(verbose_name="项目实施开始时间")
    ss_end_date = models.DateField(verbose_name="项目实施结束时间")
    cy_start_date = models.DateField(verbose_name="项目初验开始时间")
    cy_end_date = models.DateField(verbose_name="项目初验结束时间")
    zy_start_date = models.DateField(verbose_name="项目终验开始时间")
    zy_end_date = models.DateField(verbose_name="项目终验结束时间")

    def __str__(self):
        return self.project_name


class File(models.Model):
    schedule_choices = (
        ("需求分析", "需求分析"),
        ("项目立项", "项目立项"),
        ("项目实施-申购", "项目申购"),
        ("项目实施-招标", "项目招标"),
        ("项目实施-入库", "设备入库"),
        ("项目实施-建设", "项目建设"),
        ("项目初验", "项目初验"),
        ("项目终验", "项目终验"),
    )
    project_schedule = models.CharField(verbose_name="项目阶段", max_length=20, choices=schedule_choices)
    file_name = models.CharField(verbose_name="资料名称", max_length=20)
    key_choices = (
        (0, "否"),
        (1, "是"),
    )
    key_file = models.SmallIntegerField(verbose_name="关键资料", choices=key_choices, default=0)

    def __str__(self):
        return self.file_name


class Project_File(models.Model):
    project = models.ForeignKey(verbose_name="项目ID", to="Project", to_field="id", on_delete=models.CASCADE)
    file = models.ForeignKey(verbose_name="资料ID", to="File", to_field="id", on_delete=models.CASCADE)
    file_status_choices = (
        ("已提交", "已提交"),
        ("未提交", "未提交"),
    )
    file_status = models.CharField(verbose_name="资料状态", max_length=20, choices=file_status_choices, default="未提交")
    deadline = models.DateField(verbose_name="计划提交时间", default="2022-01-01")
    submit_time = models.DateField(verbose_name="实际提交时间", blank=True, null=True, )
    explain = models.CharField(verbose_name="备注", max_length=20, blank=True, null=True)
    route = models.CharField(verbose_name="文件路径", max_length=50, blank=True, null=True)


class Assets(models.Model):
    project = models.ForeignKey(verbose_name="项目ID", to="Project", to_field="id", on_delete=models.CASCADE)
    contract = models.ForeignKey(verbose_name="合同ID", to="Contract", to_field="id", on_delete=models.CASCADE)
    total_type_choices = (
        (1, "硬件"),
        (2, "软件"),
        (3, "其他"),
    )
    assets_total_type = models.SmallIntegerField(verbose_name="总体类型", choices=total_type_choices)
    detail_type_choices = (
        (1, "机房基础设备"),
        (2, "IP网络设备"),
        (3, "监播设备"),
        (4, "服务器"),
        (5, "软件"),
    )
    assets_detail_type = models.SmallIntegerField(verbose_name="分项类型", choices=detail_type_choices)
    assets_name = models.CharField(verbose_name="资产名称", max_length=50)
    assets_brand = models.CharField(verbose_name="技术规格", max_length=50)
    assets_code = models.CharField(verbose_name="资产条码", max_length=20, null=True, blank=True)
    assets_sn = models.CharField(verbose_name="序列号", max_length=50, null=True, blank=True)
    assets_date = models.DateField(verbose_name="购置时间", null=True, blank=True)
    assets_room = models.CharField(verbose_name="所属机房", max_length=50, null=True, blank=True)
    assets_cabinet = models.CharField(verbose_name="所属机柜", max_length=20, null=True, blank=True)
    status_choices = (
        (1, "在线"),
        (2, "在库"),
        (3, "维修"),
        (4, "报废"),
        (5, "待入库"),
    )
    assets_status = models.SmallIntegerField(verbose_name="当前状态", choices=status_choices)
    assets_ip = models.CharField(verbose_name="网管地址", max_length=20, null=True, blank=True)
    assets_price = models.DecimalField(verbose_name="资产价格", max_digits=10, decimal_places=2)


class Contract(models.Model):
    project_id = models.IntegerField(verbose_name="项目ID")
    contract_name = models.CharField(verbose_name="合同名称", max_length=20)
    contract_code = models.CharField(verbose_name="合同编号", max_length=20)
    warehouse_price = models.DecimalField(verbose_name="已入库金额", max_digits=10, decimal_places=2, null=True)
    contract_price = models.DecimalField(verbose_name="合同金额", max_digits=10, decimal_places=2)
    apply_price = models.DecimalField(verbose_name="申购分项预算", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.contract_name


class Inspect(models.Model):
    user = models.CharField(verbose_name="巡检人员", max_length=20)
    equip = models.CharField(verbose_name="巡检设备", max_length=20)
    location = models.CharField(verbose_name="巡检位置", max_length=20)
    date = models.DateTimeField(verbose_name="巡检时间")


class User(models.Model):
    user_name = models.CharField(verbose_name="用户名", max_length=20)
    user_password = models.CharField(verbose_name="用户密码", max_length=32)
    level_choices = (
        (1, "管理员"),
        (2, "普通用户"),
        (3, "日常"),
    )
    user_level = models.SmallIntegerField(verbose_name="角色", choices=level_choices)
