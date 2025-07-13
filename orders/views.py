from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import PurchaseVoucher, PurchaseVoucherItem
from .forms import PurchaseVoucherForm, PurchaseVoucherItemForm
from django.http import JsonResponse
from common.models import Product, Address
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



class PurchaseVoucherListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'orders.view_purchasevoucher'
    model = PurchaseVoucher
    template_name = 'purchasevouchers/purchasevoucher_list.html'

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
def PurchaseVoucherAddPage(request):
    if request.method == 'POST':
        form = PurchaseVoucherForm(request.POST)
        if form.is_valid():
            purchase_voucher = form.save()
            return redirect('purchasevoucher_list')
    else:
        form = PurchaseVoucherForm()
    
    return render(request, 'purchasevouchers/purchasevoucher_form.html', {'form': form})

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


def next_serial(request):
    yyyymmdd = request.GET.get('date')
    prefix = yyyymmdd
    # 找出今天最大流水號
    latest = PurchaseVoucher.objects.filter(voucher_number__startswith=prefix).order_by('-voucher_number').first()
    if latest and latest.voucher_number[8:]:
        last_serial = int(latest.voucher_number[8:])
    else:
        last_serial = 0
    return JsonResponse({'serial': last_serial + 1})
