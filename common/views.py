from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Employee, EmployeeProfile, EmployeeContact
from django.forms import modelform_factory

EmployeeForm = modelform_factory(Employee, exclude=[])
EmployeeProfileForm = modelform_factory(EmployeeProfile, exclude=['employee'])
EmployeeContactForm = modelform_factory(EmployeeContact, exclude=['employee'])


@permission_required('common.view_employee', raise_exception=True)
@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
@permission_required('common.view_employee', raise_exception=True)
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
@permission_required('common.add_employee', raise_exception=True)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        profile_form = EmployeeProfileForm(request.POST)
        contact_form = EmployeeContactForm(request.POST)
        if form.is_valid() and profile_form.is_valid() and contact_form.is_valid():
            employee = form.save()
            profile = profile_form.save(commit=False)
            profile.employee = employee
            profile.save()
            contact = contact_form.save(commit=False)
            contact.employee = employee
            contact.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
        profile_form = EmployeeProfileForm()
        contact_form = EmployeeContactForm()
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'profile_form': profile_form,
        'contact_form': contact_form,
    })

@login_required
@permission_required('common.change_employee', raise_exception=True)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    profile = getattr(employee, 'profile', None)
    contact = getattr(employee, 'contact', None)

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
    })


@login_required
@permission_required('common.delete_employee', raise_exception=True)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
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