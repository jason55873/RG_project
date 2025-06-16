from django import forms
from .models import PurchaseVoucher, PurchaseVoucherItem
from common.models import Address, Product

class PurchaseVoucherForm(forms.ModelForm):
    class Meta:
        model = PurchaseVoucher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 根據選擇的 supplier 過濾地址
        if 'supplier' in self.data:
            try:
                supplier_id = int(self.data.get('supplier'))
                self.fields['supplier_address'].queryset = Address.objects.filter(
                    content_type__model='supplier', object_id=supplier_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['supplier_address'].queryset = Address.objects.filter(
                content_type__model='supplier', object_id=self.instance.supplier_id
            )
        else:
            self.fields['supplier_address'].queryset = Address.objects.none()

class PurchaseVoucherItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseVoucherItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 商品編號自動帶出品名、單價、計量單位
        self.fields['product'].widget.attrs.update({'class': 'product-select'})