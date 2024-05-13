from django.db import models

# Create your models here.
class Vendor_Details(models.Model):
    name = models.CharField(max_length=200)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True, max_length=50)
    on_time_delivery_rate = models.FloatField(default=0)
    quallity_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
    

class PO(models.Model):
    status_choices = (
        ('pending', 'pending'),
        ('completed', 'completed'),
        ('canceled', 'canceled'),
    )
    po_number = models.CharField(unique=True, max_length=50, default=id)
    vendor = models.ForeignKey('Vendor_Details', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=status_choices)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return f'Order: {self.po_number} - {self.vendor.name}'


class Historic_Performance(models.Model):
    vendor = models.ForeignKey('Vendor_Details', on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f'{self.vendor.name} - {self.date}'