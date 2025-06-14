from decimal import Decimal
from django import forms
from .models import (
    Employee,
    EmployeeProfile,
    EmployeeContact,
    Department,
    Warehouse,
    ProductCategory,
    Product,
    Currency,
    Supplier,
    SupplierCategory,
    Address
)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user', 'is_deleted']

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        exclude = ['employee']

class EmployeeContactForm(forms.ModelForm):
    class Meta:
        model = EmployeeContact
        exclude = ['employee']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        exclude = ['is_deleted']

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        exclude = ['is_deleted']

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        exclude = ['is_deleted']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['is_deleted']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:  # 新增時才設定預設值
            decimal_fields = [
                'msrp', 'price_a', 'price_b', 'price_c', 'price_d', 'price_e',
                'standard_cost', 'cost_rmb', 'cost_usd', 'package1_qty', 'package2_qty'
            ]
            for field_name in decimal_fields:
                if field_name in self.fields:
                    self.fields[field_name].initial = Decimal('0.000')
                    self.fields['currency'].initial = self.fields['currency'].queryset.first()

class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class SupplierCategoryForm(forms.ModelForm):
    class Meta:
        model = SupplierCategory
        fields = '__all__'


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["code", "address", "postal_code", "contact_person", "contact_title", "phone", "fax", "note"]
        widgets = {
            'note': forms.TextInput(),  # 不加 class
        }