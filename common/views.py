from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory, modelformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Employee, Department, Warehouse, ProductCategory, Product, Currency, ProductDetail, Supplier, SupplierCategory, Address
from django.forms import modelform_factory
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from .serializers import SupplierSerializer, SupplierCategorySerializer, CurrencySerializer, AddressSerializer




from .forms import (
    EmployeeForm,
    EmployeeProfileForm,
    EmployeeContactForm,
    DepartmentForm,
    WarehouseForm,
    ProductCategoryForm,
    ProductForm,
    CurrencyForm,
    SupplierForm,
    SupplierCategoryForm,
    AddressForm
)

# 員工 Employee CRUD 視圖

@login_required
@permission_required('common.view_employee', raise_exception=True)
def employee_list(request):

    employees = Employee.objects.filter(is_deleted=False)
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
@permission_required('common.add_employee', raise_exception=True)
def employee_create(request):
    username = request.POST.get('username', '') if request.method == 'POST' else ''
    if request.method == 'POST':
        last_emp = Employee.objects.order_by('-id').first()
        if last_emp:
            next_emp_id = f"{int(last_emp.employee_id) + 1:03d}"
        else:
            next_emp_id = "001"

        form = EmployeeForm(request.POST)
        form.fields['employee_id'].widget.attrs['readonly'] = True
        profile_form = EmployeeProfileForm(request.POST)
        contact_form = EmployeeContactForm(request.POST)
        if form.is_valid() and profile_form.is_valid() and contact_form.is_valid() and username:
            employee = form.save(commit=False)
            employee.employee_id = next_emp_id
            employee.save()
            profile = profile_form.save(commit=False)
            profile.employee = employee
            profile.save()
            contact = contact_form.save(commit=False)
            contact.employee = employee
            contact.save()
            # 建立對應 User 帳號
            user = User.objects.create_user(
                username=username,
                first_name=employee.name_chinese,
                password=employee.employee_id  # 預設密碼為員工編號，可改為亂數或表單輸入
            )
            employee.user = user
            employee.save()
            return redirect('employee_list')
    else:
        last_emp = Employee.objects.order_by('-id').first()
        if last_emp:
            next_emp_id = f"{int(last_emp.employee_id) + 1:03d}"
        else:
            next_emp_id = "001"

        form = EmployeeForm(initial={'employee_id': next_emp_id})
        form.fields['employee_id'].widget.attrs['readonly'] = True
        profile_form = EmployeeProfileForm()
        contact_form = EmployeeContactForm()
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'profile_form': profile_form,
        'contact_form': contact_form,
        'username': username,
    })

@login_required
@permission_required('common.change_employee', raise_exception=True)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    profile = getattr(employee, 'profile', None)
    contact = getattr(employee, 'contact', None)
    username = employee.user.username if employee.user else ''

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        profile_form = EmployeeProfileForm(request.POST, instance=profile)
        contact_form = EmployeeContactForm(request.POST, instance=contact)
        if form.is_valid() and profile_form.is_valid() and contact_form.is_valid():
            form.save()
            profile_form.save()
            contact_form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
        profile_form = EmployeeProfileForm(instance=profile)
        contact_form = EmployeeContactForm(instance=contact)
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'profile_form': profile_form,
        'contact_form': contact_form,
        'username': username,
    })


@login_required
@permission_required('common.delete_employee', raise_exception=True)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.is_deleted = True
        employee.save()
        if employee.user:
            employee.user.is_active = False
            employee.user.save()
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # 登入成功後導向首頁（請依實際頁面修改）
        else:
            messages.error(request, "帳號或密碼錯誤")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('login')  # 登出後導回登入頁

# 部門 Department CRUD 視圖

from django.urls import reverse


@login_required
@permission_required('common.view_department', raise_exception=True)
def department_list(request):
    departments = Department.objects.filter(is_deleted=False)
    return render(request, 'departments/department_list.html', {'departments': departments})


@login_required
@permission_required('common.add_department', raise_exception=True)
def department_create(request):
    from .models import Department
    if request.method == 'POST':
        # 自動產生下一個部門編號
        last_dept = Department.objects.order_by('-id').first()
        if last_dept and last_dept.code and last_dept.code.startswith('D'):
            try:
                last_num = int(last_dept.code.replace('D', ''))
            except ValueError:
                last_num = 0
            next_code = f"D{last_num + 1:03d}"
        else:
            next_code = "D001"

        form = DepartmentForm(request.POST)
        # 設定 code 欄位為 readonly
        form.fields['code'].widget.attrs['readonly'] = True
        if form.is_valid():
            dept = form.save(commit=False)
            dept.code = next_code  # 強制指定 code
            dept.save()
            return redirect('department_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f"{error}")
                    else:
                        messages.error(request, f"{field}: {error}")
    else:
        last_dept = Department.objects.order_by('-id').first()
        if last_dept and last_dept.code and last_dept.code.startswith('D'):
            try:
                last_num = int(last_dept.code.replace('D', ''))
            except ValueError:
                last_num = 0
            next_code = f"D{last_num + 1:03d}"
        else:
            next_code = "D001"

        form = DepartmentForm(initial={'code': next_code})
        form.fields['code'].widget.attrs['readonly'] = True
    return render(request, 'departments/department_form.html', {'form': form})


@login_required
@permission_required('common.change_department', raise_exception=True)
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        form.fields['code'].widget.attrs['readonly'] = True
        if form.is_valid():
            form.save()
            return redirect('department_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f"{error}")
                    else:
                        messages.error(request, f"{field}: {error}")
    else:
        form = DepartmentForm(instance=department)
        form.fields['code'].widget.attrs['readonly'] = True
    return render(request, 'departments/department_form.html', {'form': form})


@login_required
@permission_required('common.delete_department', raise_exception=True)
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.is_deleted = True
        department.save()
        return redirect('department_list')
    return render(request, 'departments/department_confirm_delete.html', {'department': department})

# 倉庫 Warehouse CRUD 視圖

@login_required
@permission_required('common.view_warehouse', raise_exception=True)
def warehouse_list(request):
    warehouses = Warehouse.objects.filter(is_deleted=False)
    return render(request, 'warehouses/warehouse_list.html', {'warehouses': warehouses})

@login_required
@permission_required('common.add_warehouse', raise_exception=True)
def warehouse_create(request):
    if request.method == 'POST':
        last_warehouse = Warehouse.objects.order_by('-id').first()
        if last_warehouse and last_warehouse.code and last_warehouse.code.startswith('W'):
            try:
                last_num = int(last_warehouse.code.replace('W', ''))
            except ValueError:
                last_num = 0
            next_code = f"W{last_num + 1:03d}"
        else:
            next_code = "W001"

        form = WarehouseForm(request.POST)
        form.fields['code'].widget.attrs['readonly'] = True
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.code = next_code  # 強制指定 code
            warehouse.save()
            return redirect('warehouse_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f"{error}")
                    else:
                        messages.error(request, f"{field}: {error}")
    else:
        last_warehouse = Warehouse.objects.order_by('-id').first()
        if last_warehouse and last_warehouse.code and last_warehouse.code.startswith('W'):
            try:
                last_num = int(last_warehouse.code.replace('W', ''))
            except ValueError:
                last_num = 0
            next_code = f"W{last_num + 1:03d}"
        else:
            next_code = "W001"

        form = WarehouseForm(initial={'code': next_code})
        form.fields['code'].widget.attrs['readonly'] = True

    return render(request, 'warehouses/warehouse_form.html', {'form': form, 'is_edit': False})

@login_required
@permission_required('common.change_warehouse', raise_exception=True)
def warehouse_update(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        form.fields['code'].widget.attrs['readonly'] = True
        if form.is_valid():
            form.save()
            return redirect('warehouse_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f"{error}")
                    else:
                        messages.error(request, f"{field}: {error}")
    else:
        form = WarehouseForm(instance=warehouse)
        form.fields['code'].widget.attrs['readonly'] = True
    return render(request, 'warehouses/warehouse_form.html', {'form': form, 'is_edit': True})

@login_required
@permission_required('common.delete_warehouse', raise_exception=True)
def warehouse_delete(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        warehouse.is_deleted = True
        warehouse.save()
        return redirect('warehouse_list')
    return render(request, 'warehouses/warehouse_confirm_delete.html', {'warehouse': warehouse})



# 產品類別 ProductCategory CRUD 視圖

@login_required
@permission_required('common.view_productcategory', raise_exception=True)
def productcategory_list(request):
    categories = ProductCategory.objects.filter(is_deleted=False)
    return render(request, 'productcategories/productcategory_list.html', {'categories': categories})

@login_required
@permission_required('common.add_productcategory', raise_exception=True)
def productcategory_create(request):
    last_category = ProductCategory.objects.order_by('-id').first()
    if last_category and last_category.code.isdigit():
        next_code = f"{int(last_category.code) + 1:03d}"
    else:
        next_code = "001"

    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        form.fields['code'].widget.attrs['readonly'] = True
        if form.is_valid():
            category = form.save(commit=False)
            category.code = next_code
            category.save()
            return redirect('productcategory_list')
    else:
        form = ProductCategoryForm(initial={'code': next_code})
        form.fields['code'].widget.attrs['readonly'] = True
    return render(request, 'productcategories/productcategory_form.html', {'form': form})

@login_required
@permission_required('common.change_productcategory', raise_exception=True)
def productcategory_update(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category)
        form.fields['code'].widget.attrs['readonly'] = True
        if form.is_valid():
            form.save()
            return redirect('productcategory_list')
    else:
        form = ProductCategoryForm(instance=category)
        form.fields['code'].widget.attrs['readonly'] = True
    return render(request, 'productcategories/productcategory_form.html', {'form': form})

@login_required
@permission_required('common.delete_productcategory', raise_exception=True)
def productcategory_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category.is_deleted = True
        category.save()
        return redirect('productcategory_list')
    return render(request, 'productcategories/productcategory_confirm_delete.html', {'category': category})


# 產品 Product CRUD 視圖

@login_required
@permission_required('common.view_product', raise_exception=True)
def product_list(request):
    query = request.GET.get('q', '')
    if 'page_size' in request.GET:
        try:
            request.session['page_size'] = int(request.GET.get('page_size'))
        except (ValueError, TypeError):
            request.session['page_size'] = 10
    page_size = request.session.get('page_size', 10)

    product_qs = Product.objects.filter(is_deleted=False)
    if query:
        product_qs = product_qs.filter(
            Q(code__icontains=query) |
            Q(name__icontains=query) |
            Q(customer_barcode__icontains=query)
        )

    paginator = Paginator(product_qs.order_by('code'), page_size)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, 'products/product_list.html', {
        'products': products,
        'query': query,
        'page_size': page_size,
        'page_size_options': [10, 20, 50, 100],
    })

# Inline formset for ProductDetail
ProductDetailFormSet = inlineformset_factory(
    Product, ProductDetail,
    fields=["id","code_suffix", "value"],
    extra=0
)

@login_required
@permission_required('common.add_product', raise_exception=True)
def product_create(request):
    product = Product()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        form.fields['category'].queryset = ProductCategory.objects.filter(is_deleted=False)
        form.fields['currency'].queryset = Currency.objects.filter(is_deleted=False)
        formset = ProductDetailFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            return redirect('product_list')
    else:
        form = ProductForm()
        form.fields['category'].queryset = ProductCategory.objects.filter(is_deleted=False)
        form.fields['currency'].queryset = Currency.objects.filter(is_deleted=False)
        formset = ProductDetailFormSet(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'formset': formset,
        'is_edit': False,
    })

@login_required
@permission_required('common.change_product', raise_exception=True)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        form.fields['category'].queryset = ProductCategory.objects.filter(is_deleted=False)
        form.fields['currency'].queryset = Currency.objects.filter(is_deleted=False)
        formset = ProductDetailFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        form.fields['category'].queryset = ProductCategory.objects.filter(is_deleted=False)
        form.fields['currency'].queryset = Currency.objects.filter(is_deleted=False)
        formset = ProductDetailFormSet(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'formset': formset,
        'is_edit': True,
    })

@login_required
@permission_required('common.delete_product', raise_exception=True)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_deleted = True
        product.save()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


# 貨幣 Currency CRUD 視圖
CurrencyForm = modelform_factory(Currency, exclude=[])

@login_required
@permission_required('common.view_currency', raise_exception=True)
def currency_list(request):
    currencies = Currency.objects.all()
    return render(request, 'currencies/currency_list.html', {'currencies': currencies})

@login_required
@permission_required('common.add_currency', raise_exception=True)
def currency_create(request):
    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('currency_list')
    else:
        form = CurrencyForm()
    return render(request, 'currencies/currency_form.html', {'form': form, 'is_edit': False})

@login_required
@permission_required('common.change_currency', raise_exception=True)
def currency_update(request, pk):
    currency = get_object_or_404(Currency, pk=pk)
    if request.method == 'POST':
        form = CurrencyForm(request.POST, instance=currency)
        if form.is_valid():
            form.save()
            return redirect('currency_list')
    else:
        form = CurrencyForm(instance=currency)
    return render(request, 'currencies/currency_form.html', {'form': form, 'is_edit': True})

@login_required
@permission_required('common.delete_currency', raise_exception=True)
def currency_delete(request, pk):
    currency = get_object_or_404(Currency, pk=pk)
    if request.method == 'POST':
        currency.delete()
        return redirect('currency_list')
    return render(request, 'currencies/currency_confirm_delete.html', {'currency': currency})


@login_required
@permission_required('common.view_product', raise_exception=True)
def product_list_api(request):
    query = request.GET.get('q', '')
    field = request.GET.get('field', 'all')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))

    products_qs = Product.objects.filter(is_deleted=False)

    if query:
        if field == 'code':
            products_qs = products_qs.filter(code__istartswith=query)
        elif field == 'name':
            products_qs = products_qs.filter(name__icontains=query)
        elif field == 'customer_barcode':
            products_qs = products_qs.filter(customer_barcode__istartswith=query)
        else:
            products_qs = products_qs.filter(
                Q(code__icontains=query) |
                Q(name__icontains=query) |
                Q(customer_barcode__icontains=query)
            )

    paginator = Paginator(products_qs.order_by('code'), page_size)
    page_obj = paginator.get_page(page)

    results = []
    for p in page_obj:
        results.append({
            'id': p.id,
            'code': p.code,
            'customer_barcode': p.customer_barcode,
            'name': p.name,
            'category': p.category.name if p.category else '',
            'price_a': str(p.price_a),
            'price_b': str(p.price_b),
            'standard_cost': str(p.standard_cost),
            'unit': p.unit,
            'msrp': str(p.msrp),
            'currency': p.currency.short_name if p.currency else '',
            'barcode': p.barcode,
        })

    return JsonResponse({
        'count': paginator.count,
        'page': page_obj.number,
        'page_size': page_size,
        'results': results
    })


@login_required
@permission_required('common.view_suppliercategory', raise_exception=True)
def suppliercategory_list(request):
    categories = SupplierCategory.objects.all()
    return render(request, 'suppliers/suppliercategory_list.html', {'categories': categories})

@login_required
@permission_required('common.add_suppliercategory', raise_exception=True)
def suppliercategory_create(request):
    if request.method == 'POST':
        form = SupplierCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suppliercategory_list')
    else:
        form = SupplierCategoryForm()
    return render(request, 'suppliers/suppliercategory_form.html', {'form': form})

@login_required
@permission_required('common.change_suppliercategory', raise_exception=True)
def suppliercategory_update(request, pk):
    category = get_object_or_404(SupplierCategory, pk=pk)
    if request.method == 'POST':
        form = SupplierCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('suppliercategory_list')
    else:
        form = SupplierCategoryForm(instance=category)
    return render(request, 'suppliers/suppliercategory_form.html', {'form': form})

@login_required
@permission_required('common.delete_suppliercategory', raise_exception=True)
def suppliercategory_delete(request, pk):
    category = get_object_or_404(SupplierCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('suppliercategory_list')
    return render(request, 'suppliers/suppliercategory_confirm_delete.html', {'category': category})


# Supplier CRUD 視圖

AddressFormSet = modelformset_factory(
    Address,
    form=AddressForm,
    fields=["code", "address", "postal_code", "contact_person", "contact_title", "phone", "fax", "note"],
    extra=0
)


@login_required
@permission_required('common.view_supplier', raise_exception=True)
def supplier_list(request):
    suppliers = Supplier.objects.filter(is_deleted=False) if hasattr(Supplier, 'is_deleted') else Supplier.objects.all()
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})

@login_required
@permission_required('common.add_supplier', raise_exception=True)
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        formset = AddressFormSet(request.POST, queryset=Address.objects.none())
        if form.is_valid() and formset.is_valid():
            supplier = form.save()
            content_type = ContentType.objects.get_for_model(Supplier)
            for f in formset:
                if f.cleaned_data and not f.cleaned_data.get('DELETE', False):
                    address = f.save(commit=False)
                    address.content_type = content_type
                    address.object_id = supplier.id
                    address.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
        formset = AddressFormSet(queryset=Address.objects.none())

    return render(request, 'suppliers/supplier_form.html', {
        'form': form,
        'formset': formset,
        'is_edit': False
    })

@login_required
@permission_required('common.change_supplier', raise_exception=True)
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    content_type = ContentType.objects.get_for_model(Supplier)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        formset = AddressFormSet(request.POST, queryset=supplier.addresses.all())
        if form.is_valid() and formset.is_valid():
            form.save()
            for f in formset:
                if f.cleaned_data:
                    if f.cleaned_data.get('DELETE', False):
                        if f.instance.pk:
                            f.instance.delete()
                    else:
                        address = f.save(commit=False)
                        address.content_type = content_type
                        address.object_id = supplier.id
                        address.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
        formset = AddressFormSet(queryset=supplier.addresses.all())

    return render(request, 'suppliers/supplier_form.html', {
        'form': form,
        'formset': formset,
        'is_edit': True
    })

@login_required
@permission_required('common.delete_supplier', raise_exception=True)
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        if hasattr(supplier, 'is_deleted'):
            supplier.is_deleted = True
            supplier.save()
        else:
            supplier.delete()
        return redirect('supplier_list')
    return render(request, 'suppliers/supplier_confirm_delete.html', {'supplier': supplier})

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SupplierCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SupplierCategory.objects.all()
    serializer_class = SupplierCategorySerializer

class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer