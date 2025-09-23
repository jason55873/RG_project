from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('purchasevoucher/', views.PurchaseVoucherListView.as_view(), name='purchasevoucher_list'),
    path('purchasevouchers/init/', views.purchasevoucher_init, name='purchasevoucher_init_api'),
    path('purchasevoucher/add/', views.PurchaseVoucherAddPage, name='purchasevoucher_add'),
    path('purchasevoucher/<int:pk>/edit/', views.PurchaseVoucherAddPage, name='PurchaseVoucherEditPage'),
    path('purchasevoucher/<int:pk>/delete/', views.PurchaseVoucherDeleteView.as_view(), name='purchasevoucher_delete'),
    path('purchasevoucher/ajax/address_detail/', views.address_detail, name='address_detail'),
    path('purchasevoucher/ajax/product_detail/', views.product_detail, name='product_detail'),
    path('purchasevouchers/<int:pk>/', api_views.purchasevoucher_detail, name='purchasevoucher_detail'),
    path('next_serial/', views.next_serial, name='api_purchasevoucher_next_serial'),
    path('currencies/', api_views.CurrencyListAPIView.as_view(), name='api_currency_list'),
    path('suppliers/', api_views.SupplierListAPIView.as_view(), name='api_supplier_list'),
    path('employees/', api_views.EmployeeListAPIView.as_view(), name='api_employee_list'),
    path('product_lookup/', api_views.product_lookup, name='product_lookup'),
    path('purchasevouchers/', api_views.PurchaseVoucherCreateAPIView.as_view(), name='api_purchasevoucher_create'),

]