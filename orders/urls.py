from django.urls import path
from . import views

urlpatterns = [
    path('purchasevoucher/', views.PurchaseVoucherListView.as_view(), name='purchasevoucher_list'),
    path('purchasevoucher/add/', views.PurchaseVoucherCreateView.as_view(), name='purchasevoucher_add'),
    path('purchasevoucher/<int:pk>/edit/', views.PurchaseVoucherUpdateView.as_view(), name='purchasevoucher_edit'),
    path('purchasevoucher/<int:pk>/delete/', views.PurchaseVoucherDeleteView.as_view(), name='purchasevoucher_delete'),
    path('purchasevoucher/ajax/address_detail/', views.address_detail, name='address_detail'),
    path('purchasevoucher/ajax/product_detail/', views.product_detail, name='product_detail'),
]