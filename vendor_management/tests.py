from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .utils import *
from django.utils import timezone

class VendorModelTestCase(TestCase):
    def setUp(self):
        # Create a test Vendor object
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Contact Details",
            address="Vendor Address",
            vendor_code="VENDOR001"
        )

    def test_vendor_creation(self):
        # Test Vendor object string representation
        self.assertEqual(self.vendor.__str__(), "Test Vendor")
        # Test initial values of performance metrics
        self.assertEqual(self.vendor.on_time_delivery_rate, 0)
        self.assertEqual(self.vendor.quality_rating_avg, 0)
        self.assertEqual(self.vendor.average_response_time, 0)
        self.assertEqual(self.vendor.fulfillment_rate, 0)


class PurchaseOrderModelTestCase(TestCase):
    def setUp(self):
        # Create a test Vendor object
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Contact Details",
            address="Vendor Address",
            vendor_code="VENDOR001"
        )
        # Create a test PurchaseOrder object
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items=["Item 1", "Item 2"],
            quantity=10,
            status="pending",
            quality_rating=4.5,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now()
        )

    def test_purchase_order_creation(self):
        # Test PurchaseOrder object string representation
        self.assertEqual(self.purchase_order.__str__(), "PO001")


class VendorPerformanceMetricsModelTestCase(TestCase):
    def setUp(self):
        # Create a test Vendor object
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Contact Details",
            address="Vendor Address",
            vendor_code="VENDOR001"
        )
        # Create a test VendorPerformanceMetrics object
        self.performance_metrics = VendorPerformanceMetrics.objects.create(
            vendor=self.vendor,
            date=timezone.now(),
            on_time_delivery_rate=90,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=95
        )

    def test_vendor_performance_metrics_creation(self):
        # Test VendorPerformanceMetrics object creation
        self.assertEqual(self.performance_metrics.vendor, self.vendor)


class UtilsFunctionsTestCase(TestCase):
    def setUp(self):
        # Create a test Vendor object
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Contact Details",
            address="Vendor Address",
            vendor_code="VENDOR001"
        )

    def test_utils_functions(self):
        # Test utility functions for calculating performance metrics
        self.assertEqual(calculate_on_time_delivery_rate(self.vendor), 0)
        self.assertEqual(calculate_quality_rating_avg(self.vendor), 0)
        self.assertEqual(calculate_average_response_time(self.vendor), 0)
        self.assertEqual(calculate_fulfillment_rate(self.vendor), 0)

class APITestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create an authentication token for the test user
        self.token = Token.objects.create(user=self.user)

        # Initialize the APIClient with token authentication
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create a test vendor
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@example.com',
            address='Test Address',
            vendor_code='TEST001',
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5,
            average_response_time=24.0,
            fulfillment_rate=98.0
        )

        # Create a test purchase order
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO-001',
            vendor=self.vendor,
            order_date='2024-04-30T12:00:00Z',
            delivery_date='2024-05-05T12:00:00Z',
            items=[{'name': 'Item 1', 'quantity': 10}],
            quantity=10,
            status='pending',
            quality_rating=None,
            issue_date='2024-04-30T12:00:00Z',
            acknowledgment_date=None
        )

    def test_purchase_order_list_create_api(self):
        url = reverse('purchase-order-list-create')
        # Change the 'delivery_date' to an invalid format to trigger a bad request
        data = {
            'po_number': 'PO-002',
            'vendor': str(self.vendor.pk),
            'order_date': '2024-04-30T12:00:00Z',
            'delivery_date': '2024-05-05T12:00:00Z',
            'items': [{'name': 'Item 2', 'quantity': 5}],
            'quantity': 5,
            'quality_rating': 5,
            'issue_date': '2024-04-30T09:07:51.312Z',
            'acknowledgment_date': '2024-04-30T09:07:51.312Z',
            'status': 'pending'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)  # Check if the purchase order is created

    def test_vendor_retrieve_update_destroy_api(self):
        url = reverse('vendor-retrieve-update-destroy', args=[self.vendor.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'name': 'Updated Vendor',
            'contact_details': 'updated_vendor@example.com',
            'address': 'Updated Address',
            'vendor_code': 'UPDATED001',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_vendor_list_create_api(self):
        url = reverse('vendor-list-create')
        data = {
            'name': 'New Vendor',
            'contact_details': 'new_vendor@example.com',
            'address': 'New Address',
            'vendor_code': 'NEW001',
            'on_time_delivery_rate': 90.0,
            'quality_rating_avg': 4.0,
            'average_response_time': 30.0,
            'fulfillment_rate': 95.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)  # Check if the vendor is created

    def test_vendor_performance_metrics_api(self):
        url = reverse('vendor-performance', args=[self.vendor.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # You can further assert the response data to ensure correct performance metrics retrieval

    def test_acknowledge_purchase_order_api(self):
        url = reverse('purchase-order-acknowledge', args=[self.purchase_order.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # You can further assert the updated acknowledgment date of the purchase order

    def test_purchase_order_retrieve_update_destroy_api(self):
        url = reverse('purchase-order-retrieve-update-destroy', args=[self.purchase_order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'po_number': 'PO-003',
            'vendor': self.vendor.pk,
            'order_date': '2024-04-30T12:00:00Z',
            'delivery_date': '2024-05-05T12:00:00Z',
            'items': [{'name': 'Item 3', 'quantity': 8}],
            'quantity': 8,
            'quality_rating': 5,
            'issue_date': '2024-04-30T09:07:51.312Z',
            'acknowledgment_date': '2024-04-30T09:07:51.312Z',
            'status': 'pending'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_access(self):
        self.client.credentials()  # Clear credentials
        url = reverse('vendor-list-create')  # Choose any protected endpoint
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_data_format(self):
        url = reverse('purchase-order-list-create')
        invalid_data = "invalid_json_data"
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_non_existent_resource_retrieval(self):
        # Attempt to retrieve a vendor with an invalid ID
        invalid_vendor_id = 99999
        vendor_url = reverse('vendor-retrieve-update-destroy', args=[invalid_vendor_id])
        vendor_response = self.client.get(vendor_url)
        self.assertEqual(vendor_response.status_code, status.HTTP_404_NOT_FOUND)

        # Attempt to retrieve a purchase order with an invalid ID
        invalid_po_id = 99999
        po_url = reverse('purchase-order-retrieve-update-destroy', args=[invalid_po_id])
        po_response = self.client.get(po_url)
        self.assertEqual(po_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_with_invalid_data(self):
        # Attempt to update a vendor with invalid data
        invalid_vendor_data = {
            'name': '',  # Invalid name
            'contact_details': 'updated_vendor@example.com',
            'address': 'Updated Address',
            'vendor_code': 'UPDATED001',
        }
        vendor_url = reverse('vendor-retrieve-update-destroy', args=[self.vendor.pk])
        response = self.client.put(vendor_url, invalid_vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class VendorPerformanceMetricsAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='Test Address', vendor_code='TEST001')

    def test_vendor_performance_metrics_api(self):
        url = reverse('vendor-performance', args=[self.vendor.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the response data here

class AcknowledgePurchaseOrderAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='Test Address', vendor_code='TEST001')
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO-001',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items=[{'name': 'Item 1', 'quantity': 10}],
            quantity=10,
            status='pending',
            quality_rating=None,
            issue_date=timezone.now(),
            acknowledgment_date=None
        )

    def test_acknowledge_purchase_order_api(self):
        url = reverse('purchase-order-acknowledge', args=[self.purchase_order.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert the acknowledgment date of the purchase order

    def test_acknowledge_purchase_order_invalid_id(self):
        url = reverse('purchase-order-acknowledge', args=[999])  # Invalid ID
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_acknowledge_purchase_order_already_acknowledged(self):
        # Set acknowledgment date to simulate an already acknowledged purchase order
        self.purchase_order.acknowledgment_date = timezone.now()
        self.purchase_order.save()
        url = reverse('purchase-order-acknowledge', args=[self.purchase_order.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Expecting OK since the request was successful

class PurchaseOrderListCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='Test Address', vendor_code='TEST001')

    def test_create_purchase_order_api(self):
        url = reverse('purchase-order-list-create')
        data = {
            'po_number': 'PO-002',
            'vendor': self.vendor.pk,
            'order_date': timezone.now(),
            'delivery_date': timezone.now(),
            'items': [{'name': 'Item 2', 'quantity': 5}],
            'quantity': 5,
            'status': 'pending',
            'issue_date': timezone.now(),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_purchase_order_invalid_data(self):
        url = reverse('purchase-order-list-create')
        invalid_data = {
            'po_number': 'PO-002',
            'vendor': self.vendor.pk,
            # Missing required fields
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)