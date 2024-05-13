from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from .models import *
from datetime import datetime

# Create your tests here.
class VendorAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_data = {
            'name': 'Test Subject',
            'contact_details': 'Details for contact',
            'address': 'Vendor Address',
            'vendor_code': 'VINC'
        }
        self.vendor = Vendor_Details.objects.create(**self.vendor_data)

    def test_vendor_list(self):
        url = reverse('vendor_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_vendor_detail(self):
        url = reverse('vendor_details', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor_data['name'])
        self.assertEqual(response.data['contact_details'], self.vendor_data['contact_details'])
        self.assertEqual(response.data['address'], self.vendor_data['address'])
        self.assertEqual(response.data['vendor_code'], self.vendor_data['vendor_code'])


class POAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.vendor = Vendor_Details.objects.create(
            name='Vendor 1',
            contact_details='Vendor contact',
            address='Vendor Address',
            vendor_code='V1'
        )

        self.PO_data = {
            'po_number': 'P1',
            'vendor': self.vendor,
            'order_date': timezone.now(),
            'delivery_date': timezone.now() + timezone.timedelta(days=5),
            'items': {
                'name':'item_name',
                'brand':'itme_brand'
                },
            'quantity': 2,
            'status': 'pending',
            'issue_date': timezone.now()
        }
        self.purhcase_order = PO.objects.create(**self.PO_data)

    def test_PO_list(self):
        url=reverse('PO_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_PO_detail(self):
        url=reverse('PO_details', args=[self.purhcase_order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], self.PO_data['po_number'])
        self.assertEqual(response.data['vendor'], self.PO_data['vendor'].id)
        self.assertEqual(response.data['order_date'], self.PO_data['order_date'].strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(response.data['status'], self.PO_data['status'])