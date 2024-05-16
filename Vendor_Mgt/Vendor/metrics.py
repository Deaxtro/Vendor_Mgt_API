from django.db.models import Avg, F, ExpressionWrapper, DurationField, FloatField
from django.utils import timezone
from .models import *

def new_on_time_delivery_rate(vendor):
    completed_purchase_orders = PO.objects.filter(vendor=vendor, status='completed')
    on_time_deliveries = completed_purchase_orders.filter(delivery_date__lte=timezone.now())
    new_otdr = (on_time_deliveries.count()/completed_purchase_orders.count())*100 if completed_purchase_orders.count()>0 else 0
    return new_otdr

def new_rating_avg(vendor):
    completed_purhcase_orders_rating = PO.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False).aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
    return completed_purhcase_orders_rating

def new_avg_resp_time(vendor):
    acknowledged_purchase_orders = PO.objects.filter(
        vendor=vendor, acknowledgment_date__isnull=False
        ).annotate(
            response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
            ).annotate(
                response_time_in_days=ExpressionWrapper(
                    F('response_time') / (86400*1000000), output_field=FloatField()
                )
            )
    avg_response_times = acknowledged_purchase_orders.aggregate(avg_response_times=Avg('response_time_in_days'))['avg_response_times']
    return avg_response_times if avg_response_times else 0

def new_fulfillment_rate(vendor):
    issued_purchase_orders = PO.objects.filter(vendor=vendor)
    fulfilled_orders = issued_purchase_orders.filter(status='completed', issue_date__lte=timezone.now())
    new_fr = (fulfilled_orders.count()/issued_purchase_orders.count())*100 if issued_purchase_orders.count()>0 else 0
    return new_fr


def update_historical_performance(vendor):
    Historic_Performance.objects.create(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=new_on_time_delivery_rate(vendor),
        quality_rating_avg=new_rating_avg(vendor),
        average_response_time=new_avg_resp_time(vendor),
        fulfillment_rate=new_fulfillment_rate(vendor)
    )

def update_all_metrics(vendor):
    vendor.on_time_delivery_rate = new_on_time_delivery_rate(vendor)
    vendor.qualtiy_rating_avg = new_rating_avg(vendor)
    vendor.average_response_time = new_avg_resp_time(vendor)
    vendor.fulfillment_rate = new_fulfillment_rate(vendor)
    vendor.save()
    update_historical_performance(vendor)
