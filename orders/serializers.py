from rest_framework import serializers
from .models import PurchaseVoucher, PurchaseVoucherItem

class PurchaseVoucherItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseVoucherItem
        fields = '__all__'

class PurchaseVoucherSerializer(serializers.ModelSerializer):
    items = PurchaseVoucherItemSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseVoucher
        fields = '__all__'