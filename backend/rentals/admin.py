from django.contrib import admin
from .models import House, Tenant, Invoice, Payment, MpesaLog


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'rent_amount', 'is_occupied')
    search_fields = ('name',)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'house', 'lease_start', 'lease_end')
    search_fields = ('name', 'phone_number')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('ref', 'tenant', 'period', 'amount_due', 'amount_paid', 'status')
    search_fields = ('ref', 'tenant__name', 'tenant__phone_number')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'receipt_number', 'mpesa_transaction_id', 'paid_at')
    search_fields = ('receipt_number', 'mpesa_transaction_id')


@admin.register(MpesaLog)
class MpesaLogAdmin(admin.ModelAdmin):
    list_display = ('kind', 'created_at')
