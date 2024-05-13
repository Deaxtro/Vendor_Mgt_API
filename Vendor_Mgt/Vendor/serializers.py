from rest_framework import serializers
from .models import PO, Historic_Performance, Vendor_Details

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Details
        fields = '__all__'


class POSerialiezer(serializers.ModelSerializer):
    class Meta:
        model = PO
        fields = '__all__'


class Historic_PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historic_Performance
        fields = '__all__'