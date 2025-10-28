# 員工業務邏輯 Service
from .entities import Employee, Department
from typing import List, Optional

class EmployeeService:
    def create_employee(self, employee: Employee):
        # 實際邏輯由 infrastructure/repository 實作
        pass

    def update_employee(self, employee: Employee):
        pass

    def delete_employee(self, employee_id: int):
        pass

    def get_employee(self, employee_id: int) -> Optional[Employee]:
        pass

    def list_employees(self) -> List[Employee]:
        pass


class DepartmentService:
    def create_department(self, department: Department):
        pass

    def update_department(self, department: Department):
        pass

    def delete_department(self, department_id: int):
        pass

    def get_department(self, department_id: int) -> Optional[Department]:
        pass

    def list_departments(self) -> List[Department]:
        pass
