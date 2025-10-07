# rentals/models.py
from django.db import models
from django.utils import timezone


class House(models.Model):
    name = models.CharField(max_length=120, unique=True)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_occupied = models.BooleanField(default=False)


def __str__(self):
    return self.name


class Tenant(models.Model):
    name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20, unique=True)
    id_number = models.CharField(max_length=20, blank=True, null=True)
    house = models.OneToOneField(House, on_delete=models.SET_NULL, null=True, blank=True)
    lease_start = models.DateField(default=timezone.now)
    lease_end = models.DateField(blank=True, null=True)


def __str__(self):
    return f"{self.name} ({self.phone_number})"


class Invoice(models.Model):
    STATUS = (
        ('DUE', 'Due'),
        ('PARTIAL', 'Partial'),
        ('PAID', 'Paid'),
        ('VOID', 'Void'),
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='invoices')
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, blank=True)
    period = models.CharField(max_length=20) # e.g. '2025-08'
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='DUE')
    ref = models.CharField(max_length=30, unique=True) # e.g. INV-2025-08-0001
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def balance(self):
        return max(self.amount_due - self.amount_paid, 0)


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=50, unique=True)
    mpesa_checkout_request_id = models.CharField(max_length=64, blank=True, null=True)
    mpesa_transaction_id = models.CharField(max_length=64, blank=True, null=True)
    raw_callback = models.JSONField(default=dict, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)


class MpesaLog(models.Model):
    kind = models.CharField(max_length=30) # 'STK_REQUEST' | 'STK_CALLBACK'
    payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
