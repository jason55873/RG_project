from django.urls import path
from . import api_views

urlpatterns = [
    path('employees/', api_views.EmployeeListAPIView.as_view(), name='api_employee_list'),
    # 其他 API 路徑...
]