from task.models import Task, Subtask, Project, File, Project_File, User, Assets, Contract
from django import forms
from utils.bootstrap import BootstrapModelForm
from django.core.exceptions import ValidationError
from utils.encrypt import md5


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = Task
        exclude = ["subtask_count", "subtask_complete_count"]

    def clean_task_name(self):
        name = self.cleaned_data["task_name"]
        if self.instance.pk is None:
            name_exists = Task.objects.filter(task_name=name).exists()
        name_exists = Task.objects.exclude(id=self.instance.pk).filter(task_name=name).exists()
        if name_exists:
            raise ValidationError("该任务已存在")
        return name


class SubtaskModelForm(BootstrapModelForm):
    class Meta:
        model = Subtask
        exclude = ["task"]


class ProjectModelForm(BootstrapModelForm):
    class Meta:
        model = Project
        exclude = ["project_status", "amount_used"]


class FileModelForm(BootstrapModelForm):
    class Meta:
        model = File
        fields = "__all__"


class ProjectfileModelForm(BootstrapModelForm):
    class Meta:
        model = Project_File
        fields = ["deadline", "submit_time", "explain"]


class UserModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = User
        fields = ["user_name", "user_password", "user_level", "confirm_password"]
        widgets = {
            "user_password": forms.PasswordInput(render_value=True)
        }

    def clean_user_name(self):
        name = self.cleaned_data["user_name"]
        if self.instance.pk is None:
            name_exists = User.objects.filter(user_name=name).exists()
        name_exists = User.objects.exclude(id=self.instance.pk).filter(user_name=name).exists()
        if name_exists:
            raise ValidationError("用户名已存在")
        return name

    def clean_user_password(self):
        password = self.cleaned_data.get("user_password")
        return md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data.get("user_password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != password:
            raise ValidationError("密码不一致")
        return confirm


class PasswordResetForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = User
        fields = ["user_password", "confirm_password"]
        widgets = {
            "user_password": forms.PasswordInput()
        }

    def clean_user_password(self):
        password = self.cleaned_data.get("user_password")
        return md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data.get("user_password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != password:
            raise ValidationError("密码不一致")
        return confirm


class LoginForm(BootstrapModelForm):
    class Meta:
        model = User
        fields = ["user_name", "user_password"]
        widgets = {
            "user_password": forms.PasswordInput(render_value=True)
        }

    def clean_user_password(self):
        password = self.cleaned_data.get("user_password")
        return md5(password)


class AssetsModelForm(BootstrapModelForm):
    class Meta:
        model = Assets
        exclude = ["project"]
        labels = {
            'contract': '合同名称',
        }

    def __init__(self, nid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contract'].choices = Contract.objects.filter(project_id=nid).distinct().values_list('id',
                                                                                                         'contract_name')


class ContractModelForm(BootstrapModelForm):
    class Meta:
        model = Contract
        exclude = ["project_id", "warehouse_price"]
