from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, SupplierCategoryViewSet, CurrencyViewSet, AddressViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'supplier_categories', SupplierCategoryViewSet)
router.register(r'currencies', CurrencyViewSet)
router.register(r'addresses', AddressViewSet)

urlpatterns = [
    # 人員資料
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    # 部門資料
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_update, name='department_update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),

    # 倉庫資料
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('warehouses/add/', views.warehouse_create, name='warehouse_create'),
    path('warehouses/<int:pk>/edit/', views.warehouse_update, name='warehouse_update'),
    path('warehouses/<int:pk>/delete/', views.warehouse_delete, name='warehouse_delete'),

    # 產品類別資料
    path('productcategories/', views.productcategory_list, name='productcategory_list'),
    path('productcategories/add/', views.productcategory_create, name='productcategory_create'),
    path('productcategories/<int:pk>/edit/', views.productcategory_update, name='productcategory_update'),
    path('productcategories/<int:pk>/delete/', views.productcategory_delete, name='productcategory_delete'),

    # 產品資料
    path('products/', views.product_list, name='product_list'),
    path('api/products/', views.product_list_api, name='product_list_api'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # 幣別資料
    path('currencies/', views.currency_list, name='currency_list'),
    path('currencies/add/', views.currency_create, name='currency_create'),
    path('currencies/<int:pk>/edit/', views.currency_update, name='currency_update'),
    path('currencies/<int:pk>/delete/', views.currency_delete, name='currency_delete'),

    # 廠商類別資料
    path('suppliercategories/', views.suppliercategory_list, name='suppliercategory_list'),
    path('suppliercategories/add/', views.suppliercategory_create, name='suppliercategory_create'),
    path('suppliercategories/<int:pk>/edit/', views.suppliercategory_update, name='suppliercategory_update'),
    path('suppliercategories/<int:pk>/delete/', views.suppliercategory_delete, name='suppliercategory_delete'),

    # 廠商資料
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),

    path('api/', include(router.urls)),

]
