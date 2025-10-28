from django.contrib import admin
from .models import Employee, Department

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'employee_name', 'department', 'email')
    search_fields = ('employee_id', 'employee_name')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_no', 'dept_name', 'parent_dept')
    search_fields = ('dept_no', 'dept_name')