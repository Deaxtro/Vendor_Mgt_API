# from asyncio.windows_events import NULL
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.db import models
# from django.http import JsonResponse
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
    permission_classes = []

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor_Details.objects.all()
    serializer_class = VendorSerializer
    permission_classes = []
    
    # def destroy(self, request, *args, **kwargs):
    #     pk = self.kwargs['pk']
    #     Vendor_Details.objects.get(pk=pk).delete()
    #     return JsonResponse(status=200, data={'message': f'Vendor with id: {pk} deleted successfully'})
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         permission_classes = []
    #     return [permission() for permission in permission_classes]

# class VendorRemoveView(generics.RetrieveDestroyAPIView):
#     queryset = Vendor_Details.objects.all()
#     serializer_class = VendorSerializer
#     permission_classes = []


class PurchaseOrderView(generics.ListCreateAPIView):
    queryset=PO.objects.all()
    serializer_class=POSerialiezer
    permission_classes=[]

class PurchaseOrderDetailview(generics.RetrieveUpdateDestroyAPIView):
    queryset=PO.objects.all()
    serializer_class=POSerialiezer
    permission_classes=[]
    # def destroy(self, request, *args, **kwargs):
    #     pk = self.kwargs['pk']
    #     PO.objects.get(pk=pk).delete()
    #     return JsonResponse(status=200, data={'message': f'Vendor with id: {pk} deleted successfully'})
    
class PerformanceDetailView(generics.RetrieveAPIView):
    queryset=Historic_Performance.objects.all()
    serializer_class=Historic_PerformanceSerializer
    permission_classes=[]

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

# @receiver(pre_save, sender=PO)
# def update_on_time_delivery_rate(sender, instance, **kwargs):
#     if instance.pk:
#         old_instance = PO.objects.get(pk=instance.pk)

#         if old_instance.status!='completed' and instance.status=='completed':
#             total_completed_orders=PO.objects.filter(vendor=instance.vendor, status='completed').count()
#             completed_before_delivery = PO.objects.filter(vendor=instance.vendor, status='completed', delivery_date__lte=instance.delivery_date).count()
#             new_on_time_delivery_date = completed_before_delivery/total_completed_orders
#             instance.vendor.on_time_delivery_date = new_on_time_delivery_date
#             instance.vendor.save()

#         if instance.quality_rating:
#             # Get the total number of completed orders for the vendor
#             total_completed_orders = PO.objects.filter(vendor=instance.vendor, status="completed").count()
            
#             # Get the sum of quality ratings for completed orders
#             total_quality_ratings = PO.objects.filter(vendor=instance.vendor, status="completed").exclude(quality_rating=None).aggregate(total_quality_ratings=models.Sum('quality_rating'))['total_quality_ratings'] or 0
#             new_quality_rating_avg=0
#             # Calculate the new quality rating average
#             try:
#                 new_quality_rating_avg = total_quality_ratings / total_completed_orders
#             except(ZeroDivisionError):
#                 new_on_time_delivery_date=0
#             # Update the vendor's quality rating average
#             instance.vendor.quality_rating_avg = new_quality_rating_avg
#             instance.vendor.save()
        
#         # Calculate average response time if acknowledgment date is provided
#         if instance.acknowledgment_date:
#             # Get the total number of completed orders for the vendor
#             total_acknowledged_orders = PO.objects.filter(vendor=instance.vendor).exclude(acknowledgment_date=None).count()
            
#             # Get the sum of response times for completed orders
#             total_response_time = PO.objects.filter(vendor=instance.vendor, status="completed").exclude(acknowledgment_date=None).aggregate(total_response_time=models.Sum(models.F('acknowledgment_date') - models.F('issue_date')))['total_response_time']
#             if total_response_time is None:
#                 total_response_time=0
#             # Calculate the new average response time
#             new_average_response_time=0
#             try:
#                 new_average_response_time = float(total_response_time / total_acknowledged_orders)
#             except(ZeroDivisionError):
#                 new_average_response_time=0
#             # Update the vendor's average response time
#             instance.vendor.average_response_time = new_average_response_time
#             instance.vendor.save()
        
#         # Calculate fulfillment rate
#         total_orders = PO.objects.filter(vendor=instance.vendor).count()
#         total_fulfilled_orders = PO.objects.filter(vendor=instance.vendor, status="completed").count()
#         new_fulfillment_rate = total_fulfilled_orders / total_orders if total_orders != 0 else 0
#         instance.vendor.fulfillment_rate = new_fulfillment_rate
#         instance.vendor.save()