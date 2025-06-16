from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import PurchaseVoucher, PurchaseVoucherItem
from .forms import PurchaseVoucherForm, PurchaseVoucherItemForm
from django.http import JsonResponse
from common.models import Product, Address

class PurchaseVoucherListView(generic.ListView):
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
