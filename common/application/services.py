# Application Service: 協調 domain/service 與 infrastructure/repository

from ..domain.entities import Employee, Department
from ..infrastructure.repositories import EmployeeRepository, DepartmentRepository
from ..domain.services import EmployeeDomainService
from typing import Optional, List

class EmployeeAppService:
    def __init__(self):
        self.repo = EmployeeRepository()
        self.domain_service = EmployeeDomainService()

    def create_employee(self, employee: Employee) -> Employee:
        errors = self.domain_service.validate_employee(employee, self.repo, is_create=True)
        if errors:
            # 可丟出自訂例外，或直接回傳錯誤
            raise ValueError(errors)
        return self.repo.create(employee, employee.username, employee.password)

    def update_employee(self, employee: Employee) -> Employee:
        errors = self.domain_service.validate_employee(employee, self.repo, is_create=False)
        if errors:
            raise ValueError(errors)
        return self.repo.update(employee)

    def delete_employee(self, employee_no: int):
        self.repo.delete(employee_no)

    def get_employee(self, id: int) -> Optional[Employee]:
        return self.repo.get_by_id(id)

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
