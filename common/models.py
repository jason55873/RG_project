from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee', verbose_name=_("帳號"))
    employee_id = models.CharField(max_length=20, unique=True, verbose_name=_("人員編號"))
    name_chinese = models.CharField(max_length=50, verbose_name=_("人員姓名"))
    gender = models.CharField(
        max_length=1,
        choices=[('M', _("男")), ('F', _("女"))],
        verbose_name=_("性別")
    )
    name_english = models.CharField(max_length=100, verbose_name=_("英文姓名"), blank=True, null=True)
    is_deleted = models.BooleanField(default=False, verbose_name=_("刪除"))

    def __str__(self):
        return f"{self.employee_id} - {self.name_chinese}"


class Department(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name=_("部門編號"))
    name = models.CharField(max_length=100, verbose_name=_("部門名稱"))
    name_en = models.CharField(max_length=100, verbose_name=_("部門英文名稱"), blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_departments', verbose_name=_("上層部門"))
    note = models.TextField(blank=True, verbose_name=_("備註"))
    is_disabled = models.BooleanField(default=False, verbose_name=_("停用"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("刪除"))

    def clean(self):
        # 避免父部門指向自己
        if self.parent == self:
            raise ValidationError("部門不能設定自己為上層部門")

        # 避免產生環狀結構
        parent = self.parent
        while parent is not None:
            if parent == self:
                raise ValidationError("父部門的層級設定產生循環，請重新設定")
            parent = parent.parent

    def __str__(self):
        return self.name


class EmployeeProfile(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(verbose_name=_("出生日期"))
    military_status = models.CharField(max_length=20, verbose_name=_("兵役"), blank=True, null=True)
    national_id = models.CharField(max_length=20, unique=True, verbose_name=_("身分證號"))
    hire_date = models.DateField(verbose_name=_("到職日期"), blank=True, null=True)
    resignation_date = models.DateField(null=True, blank=True, verbose_name=_("離職日期"))
    title_chinese = models.CharField(max_length=50, verbose_name=_("中文職稱"), blank=True, null=True)
    title_english = models.CharField(max_length=100, verbose_name=_("英文職稱"), blank=True, null=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("所屬部門"))
    blood_type = models.CharField(
        max_length=3,
        choices=[
            ('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O'),
        ],
        verbose_name=_("血型"),
        blank=True,
        null=True
    )


class EmployeeContact(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='contact')
    email = models.EmailField(verbose_name=_("Email"), blank=True, null=True)
    contact_address = models.CharField(max_length=255, verbose_name=_("聯絡地址"), blank=True, null=True)
    household_address = models.CharField(max_length=255, verbose_name=_("戶籍地址"), blank=True, null=True)
    mobile = models.CharField(max_length=20, verbose_name=_("行動電話"), blank=True, null=True)
    telephone = models.CharField(max_length=20, verbose_name=_("市話"), blank=True, null=True)

    emergency_contact_name = models.CharField(max_length=50, verbose_name=_("緊急聯絡人"), blank=True, null=True)
    emergency_contact_address = models.CharField(max_length=255, verbose_name=_("緊急聯絡人地址"), blank=True, null=True)
    emergency_contact_mobile = models.CharField(max_length=20, verbose_name=_("緊急聯絡人電話"), blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, verbose_name=_("緊急聯絡人市話"), blank=True, null=True)
