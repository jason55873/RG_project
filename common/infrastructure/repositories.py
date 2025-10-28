# 員工資料存取 Repository
from ..domain.entities import Employee
from typing import List, Optional
from django.db import transaction
from ..models import Employee as EmployeeModel, Department as DepartmentModel
# 部門資料存取 Repository
from ..domain.entities import Department
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

class DepartmentRepository:
    def create(self, department: Department):
        dept = DepartmentModel.objects.create(
            dept_no=department.dept_no,
            dept_name=department.dept_name,
            parent_dept_id=department.parent_dept_id,
            note=department.note,
            is_disabled=department.is_disabled,
            is_deleted=department.is_deleted
        )
        return dept

    def update(self, department: Department):
        dept = DepartmentModel.objects.get(id=department.id)
        dept.dept_no = department.dept_no
        dept.dept_name = department.dept_name
        dept.parent_dept_id = department.parent_dept_id
        dept.note = department.note
        dept.is_disabled = department.is_disabled
        dept.is_deleted = department.is_deleted
        dept.save()
        return dept

    def delete(self, department_id: int):
        dept = DepartmentModel.objects.get(id=department_id)
        dept.is_deleted = True
        dept.save()

    def get(self, department_id: int) -> Optional[Department]:
        dept = DepartmentModel.objects.filter(id=department_id, is_deleted=False).first()
        if not dept:
            return None
        return Department(
            id=dept.id,
            dept_no=dept.dept_no,
            dept_name=dept.dept_name,
            parent_dept_id=dept.parent_dept_id,
            note=dept.note,
            is_disabled=dept.is_disabled,
            is_deleted=dept.is_deleted
        )

    def list(self) -> List[Department]:
        depts = DepartmentModel.objects.filter(is_deleted=False)
        return [
            Department(
                id=d.id,
                dept_no=d.dept_no,
                dept_name=d.dept_name,
                parent_dept_id=d.parent_dept_id,
                note=d.note,
                is_disabled=d.is_disabled,
                is_deleted=d.is_deleted
            ) for d in depts
        ]

class EmployeeRepository:
    def create(self, employee: Employee, username: str, password: str) -> Employee:
        with transaction.atomic():
            if not username or not password:
                raise ValueError(_("帳號 和 密碼 為必填！"))
            if not employee.employee_id:
                last_emp = EmployeeModel.objects.filter().order_by('-employee_id').first()
                if last_emp and str(last_emp.employee_id).isdigit():
                    next_id = int(last_emp.employee_id) + 1
                else:
                    next_id = 1
                employee_id = f"{next_id:05d}"
            else:
                employee_id = employee.employee_id
            user_obj = User.objects.create_user(
                username=username,
                password=password,
                first_name=employee.employee_name
            )
            emp = EmployeeModel.objects.create(
                employee_id=employee_id,
                employee_name=employee.employee_name,
                gender=employee.gender,
                birth=employee.birth,
                email=employee.email,
                mobile=employee.mobile,
                department_id=employee.department_id,
                title=employee.title,
                is_deleted=employee.is_deleted,
                military_status=employee.military_status,
                national_id=employee.national_id,
                hire_date=employee.hire_date,
                resignation_date=employee.resignation_date,
                blood_type=employee.blood_type,
                contact_address=employee.contact_address,
                household_address=employee.household_address,
                telephone=employee.telephone,
                emergency_contact_name=employee.emergency_contact_name,
                emergency_contact_address=employee.emergency_contact_address,
                emergency_contact_mobile=employee.emergency_contact_mobile,
                emergency_contact_phone=employee.emergency_contact_phone,
                user=user_obj
            )
            return Employee(
                id=emp.id,
                employee_id=emp.employee_id,
                employee_name=emp.employee_name,
                gender=emp.gender,
                username=username,
                password=None,
                birth=str(getattr(emp, 'birth', None)),
                email=emp.email,
                mobile=emp.mobile,
                department_id=emp.department_id,
                title=emp.title,
                is_deleted=emp.is_deleted,
                military_status=emp.military_status,
                national_id=emp.national_id,
                hire_date=str(getattr(emp, 'hire_date', None)),
                resignation_date=str(getattr(emp, 'resignation_date', None)),
                blood_type=emp.blood_type,
                contact_address=emp.contact_address,
                household_address=emp.household_address,
                telephone=emp.telephone,
                emergency_contact_name=emp.emergency_contact_name,
                emergency_contact_address=emp.emergency_contact_address,
                emergency_contact_mobile=emp.emergency_contact_mobile,
                emergency_contact_phone=emp.emergency_contact_phone
            )

    def update(self, employee: Employee) -> Employee:
        emp = EmployeeModel.objects.get(id=employee.id)
        emp.employee_id = employee.employee_id
        emp.employee_name = employee.employee_name
        emp.gender = employee.gender
        emp.birth = employee.birth
        emp.email = employee.email
        emp.mobile = employee.mobile
        emp.department_id = employee.department_id
        emp.title = employee.title
        emp.is_deleted = employee.is_deleted
        emp.military_status = employee.military_status
        emp.national_id = employee.national_id
        emp.hire_date = employee.hire_date
        emp.resignation_date = employee.resignation_date
        emp.blood_type = employee.blood_type
        emp.contact_address = employee.contact_address
        emp.household_address = employee.household_address
        emp.telephone = employee.telephone
        emp.emergency_contact_name = employee.emergency_contact_name
        emp.emergency_contact_address = employee.emergency_contact_address
        emp.emergency_contact_mobile = employee.emergency_contact_mobile
        emp.emergency_contact_phone = employee.emergency_contact_phone
        emp.save()
        return Employee(
            id=emp.id,
            employee_id=emp.employee_id,
            employee_name=emp.employee_name,
            gender=emp.gender,
            username=getattr(employee, 'username', None),
            password=None,
            birth=str(getattr(emp, 'birth', None)),
            email=emp.email,
            mobile=emp.mobile,
            department_id=emp.department_id,
            title=emp.title,
            is_deleted=emp.is_deleted,
            military_status=emp.military_status,
            national_id=emp.national_id,
            hire_date=str(getattr(emp, 'hire_date', None)),
            resignation_date=str(getattr(emp, 'resignation_date', None)),
            blood_type=emp.blood_type,
            contact_address=emp.contact_address,
            household_address=emp.household_address,
            telephone=emp.telephone,
            emergency_contact_name=emp.emergency_contact_name,
            emergency_contact_address=emp.emergency_contact_address,
            emergency_contact_mobile=emp.emergency_contact_mobile,
            emergency_contact_phone=emp.emergency_contact_phone
        )

    def delete(self, employee_id: int):
        emp = EmployeeModel.objects.get(id=employee_id)
        emp.is_deleted = True
        emp.save()

    def get(self, employee_id: int) -> Optional[Employee]:
        emp = EmployeeModel.objects.filter(id=employee_id, is_deleted=False).select_related('user').first()
        if not emp:
            return None
        return Employee(
            id=emp.id,
            employee_id=emp.employee_id,
            employee_name=emp.employee_name,
            gender=emp.gender,
            username=getattr(emp.user, 'username', None) if hasattr(emp, 'user') and emp.user else None,
            password=None,
            birth=str(getattr(emp, 'birth', None)),
            email=emp.email,
            mobile=emp.mobile,
            department_id=emp.department_id,
            title=emp.title,
            is_deleted=emp.is_deleted,
            military_status=emp.military_status,
            national_id=emp.national_id,
            hire_date=str(getattr(emp, 'hire_date', None)),
            resignation_date=str(getattr(emp, 'resignation_date', None)),
            blood_type=emp.blood_type,
            contact_address=emp.contact_address,
            household_address=emp.household_address,
            telephone=emp.telephone,
            emergency_contact_name=emp.emergency_contact_name,
            emergency_contact_address=emp.emergency_contact_address,
            emergency_contact_mobile=emp.emergency_contact_mobile,
            emergency_contact_phone=emp.emergency_contact_phone
        )

    def list(self) -> List[Employee]:
        emps = EmployeeModel.objects.filter(is_deleted=False).select_related('user')
        return [
            Employee(
                id=e.id,
                employee_id=e.employee_id,
                employee_name=e.employee_name,
                gender=e.gender,
                username=getattr(e.user, 'username', None) if hasattr(e, 'user') and e.user else None,
                password=None,
                birth=str(getattr(e, 'birth', None)),
                email=e.email,
                mobile=e.mobile,
                department_id=e.department_id,
                title=e.title,
                is_deleted=e.is_deleted,
                military_status=e.military_status,
                national_id=e.national_id,
                hire_date=str(getattr(e, 'hire_date', None)),
                resignation_date=str(getattr(e, 'resignation_date', None)),
                blood_type=e.blood_type,
                contact_address=e.contact_address,
                household_address=e.household_address,
                telephone=e.telephone,
                emergency_contact_name=e.emergency_contact_name,
                emergency_contact_address=e.emergency_contact_address,
                emergency_contact_mobile=e.emergency_contact_mobile,
                emergency_contact_phone=e.emergency_contact_phone
            ) for e in emps
        ]
