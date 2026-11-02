from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import PurchaseVoucherForm
from django.http import JsonResponse
from common.models import Product, Address
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PurchaseVoucher
from common.models import Currency, Supplier, Employee
from common.serializers import CurrencySerializer, SupplierSerializer, EmployeeSerializer
from django.utils import timezone


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def purchasevoucher_init(request):
    # 幣別
    currencies = Currency.objects.filter(is_deleted=False).order_by('id')
    currency_data = CurrencySerializer(currencies, many=True).data
    # 廠商
    suppliers = Supplier.objects.all().order_by('id')
    supplier_data = SupplierSerializer(suppliers, many=True).data
    # 員工
    employees = Employee.objects.filter(is_deleted=False).order_by('id')
    employee_data = EmployeeSerializer(employees, many=True).data
    # 取得今日最新流水號
    voucher_number = next_serial()
    # 現在的使用者
    current_user_id = request.user.id  # 或 request.user.pk
    return Response({
        "currencies": currency_data,
        "suppliers": supplier_data,
        "employees": employee_data,
        "today": timezone.now().date().strftime('%Y-%m-%d'),
        "current_user_id": current_user_id,
        "voucher_number": voucher_number,
    })



class PurchaseVoucherListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_purchasevoucher'
    model = PurchaseVoucher
    template_name = 'purchasevouchers/purchasevoucher_list.html'
    ordering = ['-purchase_date', '-id']  # 依日期、單號倒序排列


class PurchaseVoucherCreateView(generic.CreateView):
    model = PurchaseVoucher
    form_class = PurchaseVoucherForm
    template_name = 'purchasevouchers/purchasevoucher_form.html'
    success_url = reverse_lazy('purchasevoucher_list')

class PurchaseVoucherUpdateView(generic.UpdateView):
    model = PurchaseVoucher
    form_class = PurchaseVoucherForm
    template_name = 'purchasevouchers/purchasevoucher_form.html'
    success_url = reverse_lazy('purchasevoucher_list')

class PurchaseVoucherDeleteView(generic.DeleteView):
    model = PurchaseVoucher
    template_name = 'purchasevouchers/purchasevoucher_confirm_delete.html'
    success_url = reverse_lazy('purchasevoucher_list')

@login_required
@permission_required('order.create_PurchaseVoucher', raise_exception=True)
def PurchaseVoucherAddPage(request, pk=None):
    if request.method == 'POST':
        form = PurchaseVoucherForm(request.POST)
        if form.is_valid():
            purchase_voucher = form.save()
            return redirect('purchasevoucher_list')
    else:
        form = PurchaseVoucherForm()
    
    return render(request, 'purchasevouchers/purchasevoucher_form.html', {'form': form, 'pk': pk}) 

# Ajax: 根據 supplier_address id 取得地址、聯絡人等資訊
def address_detail(request):
    address_id = request.GET.get('address_id')
    address = get_object_or_404(Address, pk=address_id)
    data = {
        'address': address.full_address,
        'contact_person': address.contact_person,
        'title': address.title,
        'phone': address.phone,
        'fax': address.fax,
    }
    return JsonResponse(data)

# Ajax: 根據商品編號取得商品資訊
def product_detail(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, pk=product_id)
    data = {
        'name': product.name,
        'unit_price': str(product.unit_price),
        'unit': product.unit,
    }
    return JsonResponse(data)


def next_serial(data_id=None):
    if data_id:
        # 如果有傳入 data_id，則表示是編輯模式，直接返回當前流水號
        voucher = get_object_or_404(PurchaseVoucher, pk=data_id)
        return voucher.voucher_number
    today = timezone.now().date()
    prefix = today.strftime('%Y%m%d')
    # 找出今天最大流水號
    latest = PurchaseVoucher.objects.filter(voucher_number__startswith=prefix).order_by('-voucher_number').first()
    if latest and latest.voucher_number[8:]:
        last_serial = int(latest.voucher_number[8:])
    else:
        last_serial = 0
    return f'{prefix}{last_serial + 1:04d}'
