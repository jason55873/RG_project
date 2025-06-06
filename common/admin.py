from django.contrib import admin
from .models import Employee, EmployeeProfile, EmployeeContact

# Inline for 基本資料
class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    can_delete = False
    verbose_name_plural = "基本資料"
    fk_name = 'employee'

# Inline for 通訊資料
class EmployeeContactInline(admin.StackedInline):
    model = EmployeeContact
    can_delete = False
    verbose_name_plural = "通訊資料"
    fk_name = 'employee'

# 主檔 Employee 的管理介面
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name_chinese', 'gender', 'name_english')
    search_fields = ('employee_id', 'name_chinese', 'name_english')
    inlines = [EmployeeProfileInline, EmployeeContactInline]

# 可選：如果你想讓這兩張表無法單獨編輯（只透過 inline 編輯），就不用註冊它們：
# admin.site.register(EmployeeProfile)
# admin.site.register(EmployeeContact)