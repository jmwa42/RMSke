# rentals/serializers.py
from rest_framework import serializers
from .models import House, Tenant, Invoice, Payment


class HouseSerializer(serializers.ModelSerializer):
class Meta:
model = House
fields = '__all__'


class TenantSerializer(serializers.ModelSerializer):
class Meta:
model = Tenant
fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
class Meta:
model = Payment
fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
tenant = TenantSerializer(read_only=True)
payments = PaymentSerializer(many=True, read_only=True)


class Meta:
model = Invoice
fields = ['id','tenant','house','period','amount_due','amount_paid','status','ref','created_at','payments']
