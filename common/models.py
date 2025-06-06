from django.db import models
from django.utils.translation import gettext_lazy as _


class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True, verbose_name=_("Employee ID"))
    name_chinese = models.CharField(max_length=50, verbose_name=_("Chinese Name"))
    gender = models.CharField(
        max_length=1,
        choices=[('M', _("Male")), ('F', _("Female"))],
        verbose_name=_("Gender")
    )
    name_english = models.CharField(max_length=100, verbose_name=_("English Name"))

    def __str__(self):
        return f"{self.employee_id} - {self.name_chinese}"


class EmployeeProfile(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(verbose_name=_("Date of Birth"))
    military_status = models.CharField(max_length=20, verbose_name=_("Military Status"))
    national_id = models.CharField(max_length=20, unique=True, verbose_name=_("National ID"))
    hire_date = models.DateField(verbose_name=_("Hire Date"))
    resignation_date = models.DateField(null=True, blank=True, verbose_name=_("Resignation Date"))
    title_chinese = models.CharField(max_length=50, verbose_name=_("Title (Chinese)"))
    title_english = models.CharField(max_length=100, verbose_name=_("Title (English)"))
    department = models.CharField(max_length=100, verbose_name=_("Department"))
    blood_type = models.CharField(
        max_length=3,
        choices=[
            ('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O'),
        ],
        verbose_name=_("Blood Type")
    )


class EmployeeContact(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='contact')
    email = models.EmailField(verbose_name=_("Email"))
    contact_address = models.CharField(max_length=255, verbose_name=_("Contact Address"))
    household_address = models.CharField(max_length=255, verbose_name=_("Household Address"))
    mobile = models.CharField(max_length=20, verbose_name=_("Mobile Phone"))
    telephone = models.CharField(max_length=20, verbose_name=_("Telephone"))

    emergency_contact_name = models.CharField(max_length=50, verbose_name=_("Emergency Contact Name"))
    emergency_contact_address = models.CharField(max_length=255, verbose_name=_("Emergency Contact Address"))
    emergency_contact_mobile = models.CharField(max_length=20, verbose_name=_("Emergency Contact Mobile"))
    emergency_contact_phone = models.CharField(max_length=20, verbose_name=_("Emergency Contact Telephone"))
