# rentals/views.py
import base64, json, requests, datetime
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .models import House, Tenant, Invoice, Payment, MpesaLog
from .serializers import HouseSerializer, TenantSerializer, InvoiceSerializer


# --- CRUD ENDPOINTS ---
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def houses(request):
if request.method == 'GET':
return Response(HouseSerializer(House.objects.all(), many=True).data)
ser = HouseSerializer(data=request.data)
ser.is_valid(raise_exception=True)
ser.save()
return Response(ser.data)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def tenants(request):
if request.method == 'GET':
return Response(TenantSerializer(Tenant.objects.all(), many=True).data)
ser = TenantSerializer(data=request.data)
ser.is_valid(raise_exception=True)
tenant = ser.save()
if tenant.house:
tenant.house.is_occupied = True
tenant.house.save()
return Response(TenantSerializer(tenant).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_invoice(request):
tenant_id = request.data.get('tenant_id')
period = request.data.get('period') # 'YYYY-MM'
amount = request.data.get('amount')
tenant = get_object_or_404(Tenant, id=tenant_id)
ref = f"INV-{period}-{tenant.id:04d}-{int(timezone.now().timestamp())%10000:04d}"
inv = Invoice.objects.create(
tenant=tenant,
house=tenant.house,
period=period,
amount_due=amount or tenant.house.rent_amount,
ref=ref,
)
return Response(InvoiceSerializer(inv).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_invoices(request):
qs = Invoice.objects.select_related('tenant','house').order_by('-created_at')
return Response(InvoiceSerializer(qs, many=True).data)
"Amount": str(invoice.ba
