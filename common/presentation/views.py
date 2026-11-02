# Presentation 層：API 入口
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..domain.entities import Employee
from ..application.services import EmployeeAppService
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..application.services import EmployeeAppService
from ..domain.entities import Employee
from ..serializers import EmployeeSerializer

# app_service = EmployeeAppService()

def employeesPage(request):
    return render(request, 'employees/employees_list.html')


def employee_create(request):
    app_service = EmployeeAppService()
    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.POST)
        if serializer.is_valid():
            # DDD 架構：組成 Employee entity 並呼叫 application 層
            emp_data = dict(serializer.validated_data)
            employee = Employee(**emp_data)     
            try:
                created = app_service.create_employee(employee)
            except ValueError as e:
                return render(request, 'employees/employee_form.html', {'form': serializer, 'errors': e.args[0]})
            return redirect('employeesPage')
        else:
            return render(request, 'employees/employee_form.html', {'form': serializer, 'errors': serializer.errors})
    else:
        return render(request, 'employees/employee_form.html', {'form': EmployeeSerializer()})

def employee_list(request):
    app_service = EmployeeAppService()
    employees = app_service.list_employees()
    serializer = EmployeeSerializer(employees, many=True)
    return JsonResponse(serializer.data, safe=False)

def employee_update(request, pk):
    app_service = EmployeeAppService()
    if request.method == 'POST':
        emp = app_service.get_employee(int(pk))
        serializer = EmployeeSerializer(instance=emp, data=request.POST)
        if serializer.is_valid():
            emp_data = dict(serializer.validated_data)
            emp_data['employee_no'] = emp.employee_no
            employee = Employee(id=int(pk), **emp_data)
            try:
                updated = app_service.update_employee(employee)
            except ValueError as e:
                return render(request, 'employees/employee_form.html', {'form': serializer, 'errors': e.args[0]})
            return redirect('employeesPage')
        else:
            return render(request, 'employees/employee_form.html', {'form': serializer, 'errors': serializer.errors})
    else:
        emp = app_service.get_employee(int(pk))
        if not emp:
            return redirect('employeesPage')
        serializer = EmployeeSerializer(emp)
        return render(request, 'employees/employee_form.html', {'form': serializer})