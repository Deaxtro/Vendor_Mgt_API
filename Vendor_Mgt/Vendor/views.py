from .metrics import update_all_metrics
from django.utils import timezone
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import action
from .models import PO, Historic_Performance, Vendor_Details
from .serializers import VendorSerializer, POSerialiezer, Historic_PerformanceSerializer

# Create your views here.
class VendorView(generics.ListCreateAPIView):
    queryset = Vendor_Details.objects.all()
    serializer_class = VendorSerializer
    #permission_classes = []

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor_Details.objects.all()
    serializer_class = VendorSerializer
    #permission_classes = []


class PurchaseOrderView(generics.ListCreateAPIView):
    queryset=PO.objects.all()
    serializer_class=POSerialiezer
    #permission_classes=[]

class PurchaseOrderDetailview(generics.RetrieveUpdateDestroyAPIView):
    queryset=PO.objects.all()
    serializer_class=POSerialiezer
    #permission_classes=[]
    
    
class PerformanceDetailView(generics.RetrieveAPIView):
    queryset=Historic_Performance.objects.all()
    serializer_class=Historic_PerformanceSerializer
    #permission_classes=[]

class AcknowledgeView(generics.UpdateAPIView):
    queryset=PO.objects.all()
    serializer_class=POSerialiezer

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, *args, **kwargs):
        purchase_order=self.get_object()
        purchase_order.acknowledgement_date=timezone.now()
        purchase_order.save()
        update_all_metrics(purchase_order.vendor)
        return JsonResponse({'status':'200', 'message':'Order Acknowledged'})