# serializers.py
from rest_framework import serializers
from .models import Supplier, Address, SupplierCategory, Currency
from django.contrib.contenttypes.models import ContentType

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('content_type', 'object_id')  # 不讓前端傳這些


class SupplierCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierCategory
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Supplier
        fields = '__all__'

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses')
        supplier = Supplier.objects.create(**validated_data)
        content_type = ContentType.objects.get_for_model(Supplier)
        for addr_data in addresses_data:
            Address.objects.create(content_object=supplier, **addr_data)
        return supplier

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses')
        instance = super().update(instance, validated_data)

        # 刪除原有地址並重建
        content_type = ContentType.objects.get_for_model(Supplier)
        Address.objects.filter(content_type=content_type, object_id=instance.pk).delete()
        for addr_data in addresses_data:
            Address.objects.create(content_object=instance, **addr_data)
        return instance