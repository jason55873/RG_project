from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import PurchaseVoucher
from .serializers import PurchaseVoucherSerializer
from common.models import Currency, Supplier, Address, Employee, Product, ProductDetail
from common.serializers import CurrencySerializer, SupplierSerializer, EmployeeSerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseVoucher, PurchaseVoucherItem
from common.models import Product, Supplier, Address, Employee, Currency
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, Http404




# 員工清單 API
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('common.view_Employee', raise_exception=True), name='dispatch')
class EmployeeListAPIView(generics.ListAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.filter(is_deleted=False)

class PurchaseVoucherListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseVoucher.objects.all()
    serializer_class = PurchaseVoucherSerializer

class PurchaseVoucherRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseVoucher.objects.all()
    serializer_class = PurchaseVoucherSerializer

class CurrencyListAPIView(generics.ListAPIView):
    queryset = Currency.objects.filter(is_deleted=False).order_by('id')
    serializer_class = CurrencySerializer

class SupplierListAPIView(generics.ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

@api_view(['GET'])
def product_lookup(request):
    """
    依產品編號、國際條碼或客戶端條碼查詢產品資訊
    查到回傳：id, name_spec, unit, price
    """
    q = request.GET.get('q', '').strip()
    if not q:
        return Response({'error': '查詢字串不得為空'}, status=400)
    # 依據需求可擴充查詢條件
    product = Product.objects.filter(is_deleted=False).filter(Q(code=q) | Q(barcode=q) | Q(customer_barcode=q)).first()
    if not product:
        return Response({'error': '查無產品'}, status=404)
    # 取得品名規格、單位、單價（可依實際欄位調整）
    detail = ProductDetail.objects.filter(product=product).first()
    return Response({
        'id': product.id,
        'code': getattr(product, 'code', ''),
        'name_spec': getattr(product, 'name_spec', '') or getattr(product, 'name', ''),
        'unit': getattr(product, 'unit', ''),
        'price': getattr(product, 'price_a', 0)
    })

class PurchaseVoucherCreateAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            with transaction.atomic():
                # 1. 建立主單
                voucher = PurchaseVoucher.objects.create(
                    purchase_date = data.get('purchase_date'),
                    voucher_number = data.get('voucher_number'),
                    status = data.get('status'),
                    currency_id = data.get('currency'),
                    supplier_id = data.get('supplier'),
                    supplier_address_id = data.get('supplier_address'),
                    price_mode = 'no_tax' if data.get('price_mode') == 'tax_excluded' else 'tax',
                    purchaser_id = data.get('purchaser'),
                    creator_id = data.get('creator'),
                    reviewer_id = data.get('reviewer'),
                    created_at = timezone.now(),
                    updated_at = timezone.now(),
                )
                # 2. 建立明細
                items = data.get('items', [])
                for item in items:
                    # 產品查詢（可依實際欄位調整）
                    product = Product.objects.filter(id=item.get('product_id')).first()
                    if not product:
                        return Response({'error': f"查無產品：{item.get('code')}"}, status=400)
                    PurchaseVoucherItem.objects.create(
                        purchase_voucher = voucher,
                        product = product,
                        quantity = int(item.get('qty', 0)),
                        unit_price = item.get('price', 0),
                        discount = float(item.get('discount', 100)) / 100,  # 前端100代表1.00
                        is_gift = item.get('gift', False),
                    )
                return Response({'id': voucher.id, 'voucher_number': voucher.voucher_number}, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

def purchasevoucher_detail(request, pk):
    try:
        voucher = PurchaseVoucher.objects.get(pk=pk)
    except PurchaseVoucher.DoesNotExist:
        raise Http404
    items = PurchaseVoucherItem.objects.filter(purchase_voucher=voucher)
    data = {
        "id": voucher.id,
        "purchase_date": voucher.purchase_date.strftime("%Y-%m-%d"),
        "voucher_number": voucher.voucher_number,
        "status": voucher.status,
        "currency": voucher.currency_id,
        "price_mode": voucher.price_mode,
        "tax_rate": float(voucher.currency.tax_rate),
        "supplier": voucher.supplier_id,
        "supplier_address": voucher.supplier_address_id,
        "purchaser": voucher.purchaser_id,
        "creator": voucher.creator_id,
        "reviewer": voucher.reviewer_id,
        "tax_type": voucher.tax_type,
        "items": [
            {
                "code": item.product.code,
                "name": item.product.name,
                "qty": item.quantity,
                "unit": item.product.unit,
                "price": float(item.unit_price),
                "discount": float(item.discount)*100,
                "gift": item.is_gift,
                "product_id": item.product_id,
            }
            for item in items
        ]
    }
    return JsonResponse(data)


