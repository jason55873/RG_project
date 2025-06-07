from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Employee, EmployeeProfile, EmployeeContact, Department
from django.forms import modelform_factory

EmployeeForm = modelform_factory(Employee, exclude=['user', 'is_deleted'])
EmployeeProfileForm = modelform_factory(EmployeeProfile, exclude=['employee'])
EmployeeContactForm = modelform_factory(EmployeeContact, exclude=['employee'])
DepartmentForm = modelform_factory(Department, exclude=['is_deleted'])


@login_required
@permission_required('common.view_employee', raise_exception=True)
def employee_list(request):
    employees = Employee.objects.filter(is_deleted=False)
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
@permission_required('common.view_employee', raise_exception=True)
def employee_list(request):
    employees = Employee.objects.filter(is_deleted=False)
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
@permission_required('common.add_employee', raise_exception=True)
def employee_create(request):
    username = request.POST.get('username', '') if request.method == 'POST' else ''
    if request.method == 'POST':
        last_emp = Employee.objects.order_by('-id').first()
        if last_emp:
            next_emp_id = f"{int(last_emp.employee_id) + 1:03d}"
        else:
            next_emp_id = "001"

        form = EmployeeForm(request.POST)
        form.fields['employee_id'].widget.attrs['readonly'] = True
        profile_form = EmployeeProfileForm(request.POST)
        contact_form = EmployeeContactForm(request.POST)
        if form.is_valid() and profile_form.is_valid() and contact_form.is_valid() and username:
            employee = form.save(commit=False)
            employee.employee_id = next_emp_id
            employee.save()
            profile = profile_form.save(commit=False)
            profile.employee = employee
            profile.save()
            contact = contact_form.save(commit=False)
            contact.employee = employee
            contact.save()
            # 建立對應 User 帳號
            user = User.objects.create_user(
                username=username,
                first_name=employee.name_chinese,
                password=employee.employee_id  # 預設密碼為員工編號，可改為亂數或表單輸入
            )
            employee.user = user
            employee.save()
            return redirect('employee_list')
    else:
        last_emp = Employee.objects.order_by('-id').first()
        if last_emp:
            next_emp_id = f"{int(last_emp.employee_id) + 1:03d}"
        else:
            next_emp_id = "001"

        form = EmployeeForm(initial={'employee_id': next_emp_id})
        form.fields['employee_id'].widget.attrs['readonly'] = True
        profile_form = EmployeeProfileForm()
        contact_form = EmployeeContactForm()
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'profile_form': profile_form,
        'contact_form': contact_form,
        'username': username,
    })

@login_required
@permission_required('common.change_employee', raise_exception=True)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    profile = getattr(employee, 'profile', None)
    contact = getattr(employee, 'contact', None)
    username = employee.user.username if employee.user else ''

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        profile_form = EmployeeProfileForm(request.POST, instance=profile)
        contact_form = EmployeeContactForm(request.POST, instance=contact)
        if form.is_valid() and profile_form.is_valid() and contact_form.is_valid():
            form.save()
            profile_form.save()
            contact_form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
        profile_form = EmployeeProfileForm(instance=profile)
        contact_form = EmployeeContactForm(instance=contact)
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'profile_form': profile_form,
        'contact_form': contact_form,
        'username': username,
    })


@login_required
@permission_required('common.delete_employee', raise_exception=True)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.is_deleted = True
        employee.save()
        if employee.user:
            employee.user.is_active = False
            employee.user.save()
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # 登入成功後導向首頁（請依實際頁面修改）
        else:
            messages.error(request, "帳號或密碼錯誤")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('login')  # 登出後導回登入頁

# 部門 Department CRUD 視圖

from django.urls import reverse


@login_required
@permission_required('common.view_department', raise_exception=True)
def department_list(request):
    departments = Department.objects.filter(is_deleted=False)
    return render(request, 'departments/department_list.html', {'departments': departments})


@login_required
@permission_required('common.add_department', raise_exception=True)
def department_create(request):
    from .models import Department
    if request.method == 'POST':
        # 自動產生下一個部門編號
        last_dept = Department.objects.order_by('-id').first()
        if last_dept and last_dept.code and last_dept.code.startswith('D'):
            try:
                last_num = int(last_dept.code.replace('D', ''))
            except ValueError:
                last_num = 0
            next_code = f"D{last_num + 1:03d}"
        else:
            next_code = "D001"

        form = DepartmentForm(request.POST)
        # 設定 code 欄位為 readonly
        form.fields['code'].widget.attrs['readonly'] = True
        if form.is_valid():
            dept = form.save(commit=False)
            dept.code = next_code  # 強制指定 code
            dept.save()
            return redirect('department_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f"{error}")
                    else:
                        messages.error(request, f"{field}: {error}")
    else:
        last_dept = Department.objects.order_by('-id').first()
        if last_dept and last_dept.code and last_dept.code.startswith('D'):
            try:
                last_num = int(last_dept.code.replace('D', ''))
            except ValueError:
                last_num = 0
            next_code = f"D{last_num + 1:03d}"
        else:
            next_code = "D001"

        form = DepartmentForm(initial={'code': next_code})
        form.fields['code'].widget.attrs['readonly'] = True
    return render(request, 'departments/department_form.html', {'form': form})


@login_required
@permission_required('common.change_department', raise_exception=True)
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        form.fields['code'].widget.attrs['readonly'] = True
        if form.is_valid():
            form.save()
            return redirect('department_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f"{error}")
                    else:
                        messages.error(request, f"{field}: {error}")
    else:
        form = DepartmentForm(instance=department)
        form.fields['code'].widget.attrs['readonly'] = True
    return render(request, 'departments/department_form.html', {'form': form})


@login_required
@permission_required('common.delete_department', raise_exception=True)
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.is_deleted = True
        department.save()
        return redirect('department_list')
    return render(request, 'departments/department_confirm_delete.html', {'department': department})