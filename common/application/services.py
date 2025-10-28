# Application Service: 協調 domain/service 與 infrastructure/repository

from ..domain.entities import Employee, Department
from ..infrastructure.repositories import EmployeeRepository, DepartmentRepository
from typing import Optional, List

class EmployeeAppService:
    def __init__(self):
        self.repo = EmployeeRepository()

    def create_employee(self, employee: Employee) -> Employee:
        return self.repo.create(employee, employee.username, employee.password)

    def update_employee(self, employee: Employee) -> Employee:
        return self.repo.update(employee)

    def delete_employee(self, employee_id: int):
        self.repo.delete(employee_id)

    def get_employee(self, employee_id: int) -> Optional[Employee]:
        return self.repo.get(employee_id)

    def list_employees(self) -> List[Employee]:
        return self.repo.list()

class DepartmentAppService:
    def __init__(self):
        self.repo = DepartmentRepository()

    def create_department(self, department: Department):
        return self.repo.create(department)

    def update_department(self, department: Department):
        return self.repo.update(department)

    def delete_department(self, department_id: int):
        self.repo.delete(department_id)

    def get_department(self, department_id: int) -> Optional[Department]:
        return self.repo.get(department_id)

    def list_departments(self) -> List[Department]:
        return self.repo.list()
