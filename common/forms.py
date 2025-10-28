from decimal import Decimal
from django import forms
from django.forms import BaseInlineFormSet
from .models import (
    Employee,
    Department,
    Warehouse,
    ProductCategory,
    Product,
    Currency,
    Supplier,
    SupplierCategory,
    Address,
    CustomerCategory,
    Customer,
    ProductDetail
)

class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # 保留現有的 attrs，只更新 class
            existing_class = field.widget.attrs.get('class', '')
            
            if getattr(field.widget, 'input_type', None) == 'select' or field.widget.__class__.__name__ in ['Select', 'SelectMultiple']:
                new_class = 'form-select'
            else:
                new_class = 'form-control'
            
            # 合併 class，但保留其他所有 attributes（如 type: 'date'）
            if existing_class:
                field.widget.attrs['class'] = f"{existing_class} {new_class}".strip()
            else:
                field.widget.attrs['class'] = new_class


class EmployeeForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user', 'is_deleted']

# class EmployeeProfileForm(BootstrapMixin, forms.ModelForm):
#     class Meta:
#         model = EmployeeProfile
#         exclude = ['employee']
#         # widgets = {
#         #     'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
#         #     'hire_date': forms.DateInput(attrs={'type': 'date'}),
#         #     'resignation_date': forms.DateInput(attrs={'type': 'date'}),
#         # }   

# class EmployeeContactForm(BootstrapMixin, forms.ModelForm):
#     class Meta:
#         model = EmployeeContact
#         exclude = ['employee']

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

class CustomerCategoryForm(forms.ModelForm):
    class Meta:
        model = CustomerCategory
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class RequiredDetailFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        valid_count = 0
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            if form.cleaned_data.get('barcode'):
                valid_count += 1
        if valid_count == 0:
            raise forms.ValidationError("至少要有一筆商品型號且條碼必填")
        
class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = ["id", "barcode", "code_suffix", "value"]
        widgets = {
            "barcode": forms.TextInput(attrs={"required": "required"}),
        }