# serializers.py
from rest_framework import serializers
from .models import Supplier, Address, SupplierCategory, Currency, Employee
from django.contrib.contenttypes.models import ContentType

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'code', 'address', 'postal_code', 'contact_person', 'contact_title', 'phone', 'fax', 'note']

class SupplierCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierCategory
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = Supplier
        fields = [
            'id', 'code', 'full_name', 'category', 'currency', 'short_name', 'tax_id', 'invoice_title',
            'responsible_person', 'contact_person', 'phone1', 'phone2', 'phone3', 'mobile', 'fax',
            'purchaser', 'email', 'website', 'last_purchase_date', 'last_return_date', 'price_mode',
            'tax_type', 'invoice_address', 'delivery_address', 'supplier_type', 'addresses'
        ]

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        supplier = Supplier.objects.create(**validated_data)
        for address_data in addresses_data:
            Address.objects.create(content_object=supplier, **address_data)
        return supplier

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        instance = super().update(instance, validated_data)

        # Update or create addresses
        for address_data in addresses_data:
            address_id = address_data.get('id')
            if address_id:
                address = Address.objects.get(id=address_id, content_object=instance)
                for attr, value in address_data.items():
                    setattr(address, attr, value)
                address.save()
            else:
                Address.objects.create(content_object=instance, **address_data)

        return instance
    

# 員工序列化
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'name_chinese']