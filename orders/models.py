from django.db import models
from common.models import Employee, Supplier, Address, Product, Currency
from django.utils.translation import gettext_lazy as _

class PurchaseVoucher(models.Model):
    STATUS_CHOICES = [
        ('open', '未結案'),
        ('closed', '已結案'),
        ('invalid', '無效'),
    ]
    purchase_date = models.DateField(verbose_name="採購日期")
    voucher_number = models.CharField(max_length=20, unique=True, verbose_name="單據號碼")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open', verbose_name="單況")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name="幣別")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="廠商")
    supplier_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        verbose_name="廠商地址",
        limit_choices_to={'content_type__model': 'supplier'},
        related_name='purchase_vouchers'
    )
    price_mode = models.CharField(
        max_length=10,
        choices=[('no_tax', _('未稅')), ('tax', _('含稅'))],
        blank=True,
        verbose_name=_("價格模式")
    )
    purchaser = models.ForeignKey(Employee, related_name='purchase_vouchers', on_delete=models.PROTECT, verbose_name="採購人員")
    creator = models.ForeignKey(Employee, related_name='created_purchase_vouchers', on_delete=models.PROTECT, verbose_name="製單人員")
    reviewer = models.ForeignKey(Employee, related_name='reviewed_purchase_vouchers', on_delete=models.PROTECT, verbose_name="覆核人員")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True, null=True, verbose_name=_("備註"))


    def __str__(self):
        return self.voucher_number

class PurchaseVoucherItem(models.Model):
    purchase_voucher = models.ForeignKey(PurchaseVoucher, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="產品")
    quantity = models.PositiveIntegerField(verbose_name="數量")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="單價")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=1.00, verbose_name="折數")  # 1.00 代表不打折
    unreceived_quantity = models.PositiveIntegerField(default=0, verbose_name="未進貨數量")
    is_gift = models.BooleanField(default=False, verbose_name="是否為贈品")
    # 可加上產品批號、備註等欄位

    def __str__(self):
        return f"{self.product} ({self.purchase_voucher.voucher_number})"
