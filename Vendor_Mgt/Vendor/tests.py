from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from .models import *
from datetime import timedelta
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .metrics import update_all_metrics

# Create your tests here.
class VendorAPITests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
        self.token, self._ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
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
        self.user=User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
        self.token, self._ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

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


class VendorPerformanceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lenon@beatles.com', 'johnpassword')
        self.token, self._ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

        self.vendor = Vendor_Details.objects.create(
            name='Test Vendor',
            contact_details='Contact Details',
            address='address',
            vendor_code='V123'
        )
        self.purchase_order1 = PO.objects.create(
            po_number='PO123',
            vendor=self.vendor,
            order_date=timezone.now() - timedelta(days=34),
            delivery_date=timezone.now() - timedelta(days=10),
            items={"item":"test"},
            quantity=10,
            status='completed',
            quality_rating=4.0,
            issue_date=timezone.now() - timedelta(days=34),
            acknowledgment_date=timezone.now() - timedelta(days=10)
        )
        self.purchase_order2=PO.objects.create(
            po_number='PO124',
            vendor=self.vendor,
            order_date=timezone.now() - timedelta(days=5),
            delivery_date=timezone.now() + timedelta(days=2),
            items={"item": "test"},
            quantity=5,
            status='pending',
            quality_rating=None,
            issue_date=timezone.now() - timedelta(days=5),
            acknowledgment_date=None
        )

        update_all_metrics(self.vendor)
    
    def test_vendor_performance_endpoint(self):
        url=reverse('performance', args=[self.vendor.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'on_time_delivery_rate': 100.0,
            'quality_rating_avg': 4.0,
            'average_response_time': 24.0,
            'fulfillment_rate': 50.0
        }
        resp_data = {
            'on_time_delivery_rate': response.data['on_time_delivery_rate'],
            'quality_rating_avg': response.data['quality_rating_avg'],
            'average_response_time': response.data['average_response_time'],
            'fulfillment_rate': response.data['fulfillment_rate']
        }
        self.assertEqual(resp_data, expected_data)