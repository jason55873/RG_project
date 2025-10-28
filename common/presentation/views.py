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
            created = app_service.create_employee(employee)
            return redirect('employeesPage')
        else:
            return render(request, 'employees/employee_form.html', {'form': serializer, 'errors': serializer.errors})
    else:
        return render(request, 'employees/employee_form.html', {'form': EmployeeSerializer()})

# @csrf_exempt
# def employee_create(request):
#     if request.method == 'POST' and request.content_type == 'application/json':
#         data = json.loads(request.body)
#         emp = Employee(**data['employee'])
#         profile = EmployeeProfile(**data['profile'])
#         contact = EmployeeContact(**data['contact'])
#         new_emp = app_service.create_employee(emp, profile, contact)
#         return JsonResponse({'id': new_emp.id, 'employee_id': new_emp.employee_id})
#     return JsonResponse({'error': 'Method not allowed'}, status=405)

# @csrf_exempt
# def employee_update(request, pk):
#     if request.method == 'POST' and request.content_type == 'application/json':
#         data = json.loads(request.body)
#         emp = Employee(id=pk, **data['employee'])
#         profile = EmployeeProfile(employee_id=pk, **data['profile'])
#         contact = EmployeeContact(employee_id=pk, **data['contact'])
#         app_service.update_employee(emp, profile, contact)
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'error': 'Method not allowed'}, status=405)

# @csrf_exempt
# def employee_delete(request, pk):
#     if request.method == 'POST':
#         app_service.delete_employee(pk)
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'error': 'Method not allowed'}, status=405)

class EmployeeViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_service = EmployeeAppService()

    def list(self, request):
        employees = self.app_service.list_employees()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        employee = self.app_service.get_employee(int(pk))
        if not employee:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = Employee(**serializer.validated_data)
            created = self.app_service.create_employee(employee)
            return Response(EmployeeSerializer(created).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = Employee(id=int(pk), **serializer.validated_data)
            updated = self.app_service.update_employee(employee)
            return Response(EmployeeSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        self.app_service.delete_employee(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)
