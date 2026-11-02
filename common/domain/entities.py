# 員工相關 Entity
from dataclasses import dataclass
from typing import Optional

@dataclass
class Employee:
    employee_name: str
    gender: str
    username: str
    password: Optional[str] = None
    id: Optional[int] = None
    employee_no: Optional[str] = None
    birth: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    department_id: Optional[int] = None
    title: Optional[str] = None
    is_deleted: bool = False
    military_status: Optional[str] = None
    national_id: Optional[str] = None
    hire_date: Optional[str] = None
    resignation_date: Optional[str] = None
    blood_type: Optional[str] = None
    contact_address: Optional[str] = None
    household_address: Optional[str] = None
    telephone: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_address: Optional[str] = None
    emergency_contact_mobile: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

@dataclass
class Department:
    id: Optional[int]
    dept_no: str
    dept_name: str
    parent_dept_id: Optional[int]
    note: str = ""
    is_disabled: bool = False
    is_deleted: bool = False