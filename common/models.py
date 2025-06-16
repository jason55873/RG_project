from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation



class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee', verbose_name=_("帳號"))
    employee_id = models.CharField(max_length=20, unique=True, verbose_name=_("人員編號"))
    name_chinese = models.CharField(max_length=50, verbose_name=_("人員姓名"))
    gender = models.CharField(
        max_length=1,
        choices=[('M', _("男")), ('F', _("女"))],
        verbose_name=_("性別")
    )
    name_english = models.CharField(max_length=100, verbose_name=_("英文姓名"), blank=True, null=True)
    is_deleted = models.BooleanField(default=False, verbose_name=_("刪除"))

    def __str__(self):
        return f"{self.employee_id} - {self.name_chinese}"


class Department(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name=_("部門編號"))
    name = models.CharField(max_length=100, verbose_name=_("部門名稱"))
    name_en = models.CharField(max_length=100, verbose_name=_("部門英文名稱"), blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_departments', verbose_name=_("上層部門"))
    note = models.TextField(blank=True, verbose_name=_("備註"))
    is_disabled = models.BooleanField(default=False, verbose_name=_("停用"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("刪除"))

    def clean(self):
        # 避免父部門指向自己
        if self.parent == self:
            raise ValidationError("部門不能設定自己為上層部門")

        # 避免產生環狀結構
        parent = self.parent
        while parent is not None:
            if parent == self:
                raise ValidationError("父部門的層級設定產生循環，請重新設定")
            parent = parent.parent

    def __str__(self):
        return self.name


class EmployeeProfile(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(verbose_name=_("出生日期"))
    military_status = models.CharField(max_length=20, verbose_name=_("兵役"), blank=True, null=True)
    national_id = models.CharField(max_length=20, unique=True, verbose_name=_("身分證號"))
    hire_date = models.DateField(verbose_name=_("到職日期"), blank=True, null=True)
    resignation_date = models.DateField(null=True, blank=True, verbose_name=_("離職日期"))
    title_chinese = models.CharField(max_length=50, verbose_name=_("中文職稱"), blank=True, null=True)
    title_english = models.CharField(max_length=100, verbose_name=_("英文職稱"), blank=True, null=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("所屬部門"))
    blood_type = models.CharField(
        max_length=3,
        choices=[
            ('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O'),
        ],
        verbose_name=_("血型"),
        blank=True,
        null=True
    )


class EmployeeContact(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='contact')
    email = models.EmailField(verbose_name=_("Email"), blank=True, null=True)
    contact_address = models.CharField(max_length=255, verbose_name=_("聯絡地址"), blank=True, null=True)
    household_address = models.CharField(max_length=255, verbose_name=_("戶籍地址"), blank=True, null=True)
    mobile = models.CharField(max_length=20, verbose_name=_("行動電話"), blank=True, null=True)
    telephone = models.CharField(max_length=20, verbose_name=_("市話"), blank=True, null=True)

    emergency_contact_name = models.CharField(max_length=50, verbose_name=_("緊急聯絡人"), blank=True, null=True)
    emergency_contact_address = models.CharField(max_length=255, verbose_name=_("緊急聯絡人地址"), blank=True, null=True)
    emergency_contact_mobile = models.CharField(max_length=20, verbose_name=_("緊急聯絡人電話"), blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, verbose_name=_("緊急聯絡人市話"), blank=True, null=True)


class Warehouse(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name=_("倉庫編號"))
    name = models.CharField(max_length=100, verbose_name=_("倉庫名稱"))
    short_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("倉庫簡稱"))
    name_en = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("英文名稱"))
    contact_person = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("聯絡人員"))
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("聯絡電話"))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("倉庫地址"))
    note = models.TextField(blank=True, null=True, verbose_name=_("備註"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("刪除"))

    def __str__(self):
        return self.name



# Product Category model
class ProductCategory(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name=_("類別編號"))
    name = models.CharField(max_length=100, verbose_name=_("類別名稱"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("刪除"))

    def __str__(self):
        return f"{self.code} - {self.name}"


# Currency model
class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name=_("幣別編號"))
    name = models.CharField(max_length=50, verbose_name=_("幣別名稱"))
    short_name = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("幣別簡稱"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("刪除"))

    def __str__(self):
        return f"{self.code} - {self.name}"


class Address(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name=_("代碼"))
    address = models.CharField(max_length=255, verbose_name=_("地址"))
    postal_code = models.CharField(max_length=10, blank=True, verbose_name=_("郵遞區號"))
    contact_person = models.CharField(max_length=50, blank=True, verbose_name=_("聯絡人"))
    contact_title = models.CharField(max_length=50, blank=True, verbose_name=_("聯絡人職稱"))
    phone = models.CharField(max_length=50, blank=True, verbose_name=_("電話"))
    fax = models.CharField(max_length=50, blank=True, verbose_name=_("傳真"))
    note = models.TextField(blank=True, verbose_name=_("備註"))

    # Generic relation to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, verbose_name=_("內容類型"))
    object_id = models.PositiveIntegerField(null=True, verbose_name=_("對象ID"))
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _("地址")
        verbose_name_plural = _("地址")

    def __str__(self):
        return f"{self.address} ({self.code})"

# 客戶類別
class CustomerCategory(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name=_("代碼"))
    name = models.CharField(max_length=50, verbose_name=_("名稱"))
    note = models.TextField(blank=True, verbose_name=_("備註"))

    def __str__(self):
        return self.name  # 確保回傳的是名稱

# 會員等級
class MemberLevel(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name=_("代碼"))
    name = models.CharField(max_length=50, verbose_name=_("名稱"))
    note = models.TextField(blank=True, verbose_name=_("備註"))

    def __str__(self):
        return self.name  # 確保回傳的是名稱

class Member(models.Model):
    card_number = models.CharField(max_length=20, unique=True, verbose_name=_("卡號"))
    national_id = models.CharField(max_length=20, verbose_name=_("身分證號"))
    issue_date = models.DateField(verbose_name=_("發卡日期"))
    gender = models.CharField(max_length=10, verbose_name=_("性別"))
    level = models.ForeignKey(MemberLevel, on_delete=models.SET_NULL, null=True, verbose_name=_("會員等級"))
    postal_code = models.CharField(max_length=10, blank=True, verbose_name=_("郵遞區號"))
    home_address = models.ForeignKey(Address, related_name='home_members', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("戶籍地址"))
    household_address = models.ForeignKey(Address, related_name='household_members', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("居住地址"))
    addresses = GenericRelation(Address, related_query_name='member')

class Customer(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name=_("客戶代碼"))
    full_name = models.CharField(max_length=100, verbose_name=_("客戶全名"))
    category = models.ForeignKey(CustomerCategory, on_delete=models.SET_NULL, null=True, verbose_name=_("客戶類別"))
    currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True, verbose_name=_("幣別"))
    short_name = models.CharField(max_length=50, blank=True, verbose_name=_("簡稱"))
    tax_id = models.CharField(max_length=20, blank=True, verbose_name=_("統一編號"))
    invoice_title = models.CharField(max_length=100, blank=True, verbose_name=_("發票抬頭"))
    responsible_person = models.CharField(max_length=50, blank=True, verbose_name=_("負責人"))
    contact_person = models.CharField(max_length=50, blank=True, verbose_name=_("聯絡人"))
    phone1 = models.CharField(max_length=30, blank=True, verbose_name=_("電話1"))
    phone2 = models.CharField(max_length=30, blank=True, verbose_name=_("電話2"))
    phone3 = models.CharField(max_length=30, blank=True, verbose_name=_("電話3"))
    mobile = models.CharField(max_length=30, blank=True, verbose_name=_("手機"))
    fax = models.CharField(max_length=30, blank=True, verbose_name=_("傳真"))
    email = models.EmailField(blank=True, verbose_name=_("電子郵件"))
    website = models.URLField(blank=True, verbose_name=_("網站"))
    salesperson = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("業務人員"))
    last_sale_date = models.DateField(null=True, blank=True, verbose_name=_("最後銷貨日期"))
    last_return_date = models.DateField(null=True, blank=True, verbose_name=_("最後退貨日期"))
    price_mode = models.CharField(
        max_length=10,
        choices=[('no_tax', _('未稅')), ('tax', _('含稅'))],
        blank=True,
        verbose_name=_("價格模式")
    )
    tax_type = models.CharField(
        max_length=10,
        choices=[
            ('taxable', _('應稅')),
            ('exempt', _('免稅')),
            ('zero', _('零稅')),
            ('blank', _('空白')),
            ('no_invoice', _('免開'))
        ],
        blank=True,
        verbose_name=_("課稅類別")
    )
    invoice_address = models.ForeignKey(Address, related_name='invoice_customers', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("發票地址"))
    delivery_address = models.ForeignKey(Address, related_name='delivery_customers', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("送貨地址"))
    customer_type = models.CharField(max_length=50, blank=True, verbose_name=_("客戶類型"))
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("會員"))
    addresses = GenericRelation(Address, related_query_name='customer')

# 廠商類別

class SupplierCategory(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name=_("代碼"))
    name = models.CharField(max_length=50, verbose_name=_("名稱"))
    note = models.TextField(blank=True, verbose_name=_("備註"))

    def __str__(self):
        return self.name  # 確保回傳的是名稱


class Supplier(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name=_("廠商編號"))
    full_name = models.CharField(max_length=100, verbose_name=_("廠商全稱"))
    category = models.ForeignKey(SupplierCategory, on_delete=models.SET_NULL, null=True, verbose_name=_("廠商類別"))
    currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True, verbose_name=_("幣別"))
    short_name = models.CharField(max_length=50, blank=True, verbose_name=_("廠商簡稱"))
    tax_id = models.CharField(max_length=20, blank=True, verbose_name=_("統一編號"))
    invoice_title = models.CharField(max_length=100, blank=True, verbose_name=_("發票抬頭"))
    responsible_person = models.CharField(max_length=50, blank=True, verbose_name=_("負責人"))
    contact_person = models.CharField(max_length=50, blank=True, verbose_name=_("聯絡人"))
    phone1 = models.CharField(max_length=30, blank=True, verbose_name=_("聯絡電話一"))
    phone2 = models.CharField(max_length=30, blank=True, verbose_name=_("聯絡電話二"))
    phone3 = models.CharField(max_length=30, blank=True, verbose_name=_("聯絡電話三"))
    mobile = models.CharField(max_length=30, blank=True, verbose_name=_("行動電話"))
    fax = models.CharField(max_length=30, blank=True, verbose_name=_("傳真號碼"))
    purchaser = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("採購員"))
    email = models.EmailField(blank=True, verbose_name=_("電子郵件"))
    website = models.URLField(blank=True, verbose_name=_("網站"))
    last_purchase_date = models.DateField(null=True, blank=True, verbose_name=_("最近進貨日"))
    last_return_date = models.DateField(null=True, blank=True, verbose_name=_("最近退貨日"))
    price_mode = models.CharField(
        max_length=10,
        choices=[('no_tax', _('未稅')), ('tax', _('含稅'))],
        blank=True,
        verbose_name=_("產品單價")
    )
    tax_type = models.CharField(
        max_length=10,
        choices=[
            ('taxable', _('應稅')),
            ('exempt', _('免稅')),
            ('zero', _('零稅')),
            ('blank', _('空白')),
            ('no_invoice', _('免開'))
        ],
        blank=True,
        verbose_name=_("課稅類別")
    )
    invoice_address = models.ForeignKey(Address, related_name='invoice_suppliers', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("發票地址"))
    delivery_address = models.ForeignKey(Address, related_name='delivery_suppliers', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("送貨地址"))
    supplier_type = models.CharField(max_length=50, blank=True, verbose_name=_("廠商類型"))
    addresses = GenericRelation(Address, related_query_name='supplier')

    def __str__(self):
        return f"{self.code} - {self.full_name}"


# Product model
class Product(models.Model):
    code = models.CharField(max_length=30, unique=True, verbose_name=_("產品編號"))
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True, blank=True, verbose_name="廠商")
    category = models.ForeignKey('ProductCategory', on_delete=models.PROTECT, verbose_name=_("產品類別"))
    barcode = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("國際條碼"))
    customer_barcode = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("客戶端條碼"))
    name = models.CharField(max_length=200, verbose_name=_("品名規格"))
    invoice_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("發票品名"))
    english_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("英文品名"))
    unit = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("計量單位"))
    package1_qty = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, verbose_name=_("包裝1數量"))
    package1_unit = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("包裝1單位"))
    package2_qty = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, verbose_name=_("包裝2數量"))
    package2_unit = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("包裝2單位"))
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT, verbose_name=_("使用幣別"))
    msrp = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name=_("建議售價"))
    price_a = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name=_("售價A"))
    price_b = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name=_("售價B"))
    price_c = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name=_("售價C"))
    price_d = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name=_("售價D"))
    price_e = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name=_("售價E"))
    standard_cost = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name=_("標準進價"))
    cost_rmb = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True, default=0, verbose_name=_("人民幣進價"))
    cost_usd = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True, default=0, verbose_name=_("美金進價"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("刪除"))

    def __str__(self):
        return self.name


# ProductStock model
class ProductStock(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name=_("產品"))
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, verbose_name=_("倉庫編號"))
    safe_stock = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True, default=0, verbose_name=_("安全存量"))
    opening_stock = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True, default=0, verbose_name=_("期初存量"))
    current_stock = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True, default=0, verbose_name=_("現有數量"))
    real_stock = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True, default=0, verbose_name=_("實際在庫量"))
    note = models.TextField(blank=True, null=True, verbose_name=_("備註"))

    def __str__(self):
        return f"{self.product.code} - {self.warehouse.code}"


# ProductDetail model for product variants
class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='details', verbose_name=_("主商品"))
    code_suffix = models.CharField(max_length=10, verbose_name=_("型號"))  # e.g. A, B, C
    value = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("型號名稱"))  # e.g. 紅色、藍色、黃色、

    class Meta:
        unique_together = ('product', 'code_suffix')
        verbose_name = _("產品變化明細")
        verbose_name_plural = _("產品變化明細")

    def __str__(self):
        return f"{self.product.code}-{self.code_suffix} ({self.value})"