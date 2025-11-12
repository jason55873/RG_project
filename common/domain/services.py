# 員工業務邏輯 Service
from .entities import Employee, Department
from typing import List, Optional


class EmployeeDomainService:

    # 合併唯一性檢查，僅查詢一次 DB
    def check_uniqueness(self, employee, repository, exclude_id=None):
        return repository.find_duplicates(
            username=employee.username,
            email=employee.email,
            national_id=employee.national_id,
            employee_no=employee.employee_no,
            exclude_id=exclude_id
        )

    def validate_employee(self, employee, repository, is_create=True):
        errors = []
        # 必填欄位
        if not is_create and not employee.employee_no:
            errors.append("員工編號必填")

        # 修改時禁止員工編號變更
        if not is_create:
            # 取得原本資料
            db_emp = repository.get_by_id(getattr(employee, 'id', None))
            if db_emp and employee.employee_no != db_emp.employee_no:
                errors.append("員工編號不可修改")
        if not employee.employee_name:
            errors.append("姓名必填")
        if not employee.username:
            errors.append("帳號必填")
        # if not employee.department_id:
        #     errors.append("部門必填")

        # 唯一性檢查（合併查詢）
        exclude_id = None if is_create else getattr(employee, 'id', None)
        dup = self.check_uniqueness(employee, repository, exclude_id)
        if dup.get('employee_no'):
            errors.append("員工編號重複")
        if dup.get('username'):
            errors.append("帳號重複")
        if dup.get('email'):
            errors.append("Email重複")
        if dup.get('national_id'):
            errors.append("身分證字號重複")

        # Email 格式
        if employee.email:
            import re
            if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", employee.email):
                errors.append("Email格式錯誤")

        # 密碼長度（僅新增）
        # if is_create and hasattr(employee, 'password') and employee.password:
        #     if len(employee.password) < 6:
        #         errors.append("密碼長度需至少6位")

        # 部門存在性
        if employee.department_id:
            dept = repository.get_department_by_id(employee.department_id)
            if not dept:
                errors.append("部門不存在")

        # 其他業務邏輯檢查...
        return errors