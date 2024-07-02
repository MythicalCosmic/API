from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from .models import Orders, Service, Doctors, Category, Customers, CustomGroup

User = get_user_model()

class APIPermissionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a superuser
        self.superuser = User.objects.create_superuser(username='superuser', password='superpass', email='superuser@example.com')
        self.client.force_authenticate(user=self.superuser)

        # Create required related model instances
        self.category_instance = Category.objects.create(name='Some Type')

        # Create test data
        self.service = Service.objects.create(name='Test Service', typeOf=self.category_instance)
        self.doctor = Doctors.objects.create(full_name='Test Doctor')
        self.customer = Customers.objects.create(full_name='Test Customer', age=30, address='123 Main St', phone_number='555-555-5555')
        self.order_data = {
            'service': self.service.id,
            'doctor': self.doctor.id,
            'price': 100,
            'customer': self.customer.id
        }

    def test_create_order_with_superuser(self):
        url = reverse('create-order')
        response = self.client.post(url, self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_all_orders_with_superuser(self):
        url = reverse('allOrders')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
