from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order


class OrderCreationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_order_with_valid_data(self):
        data = {
            "customer": {
                "additionalStreet": "",
                "city": "Madrid",
                "companyName": "CLIENTE 1",
                "country": "ES",
                "customerType": "COMPANY",
                "email": "cliente1@cliente1.com",
                "mobilePhone": "123654789",
                "phone": "987456321",
                "postalCode": "98765",
                "street": "Calle Inventada 1",
                "NIF": "01234567L"
            },
            "orderLines": [
                {
                    "orderProduct": {
                        "name": "Producto 1",
                        "sku": "A0123456",
                        "type": "PRODUCT"
                    },
                    "quantity": 1,
                    "unitPrice": 220.14
                }
            ],
            "fiscal_position": "NATIONAL"
        }

        response = self.client.post('/store/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(id=response.data['id'])
        self.assertEqual(order.customer.companyName, 'CLIENTE 1')
        self.assertEqual(order.fiscal_position, 'NATIONAL')
        self.assertEqual(order.status, 'PRESUPUESTO')

    def test_create_order_with_invalid_email(self):
        data = {
            "customer": {
                "additionalStreet": "",
                "city": "Madrid",
                "companyName": "CLIENTE 1",
                "country": "ES",
                "customerType": "COMPANY",
                "email": "cliente1cliente1.com",  # Invalid email format
                "mobilePhone": "123654789",
                "phone": "987456321",
                "postalCode": "98765",
                "street": "Calle Inventada 1",
                "NIF": "01234567L"
            },
            "orderLines": [
                {
                    "orderProduct": {
                        "name": "Producto 1",
                        "sku": "A0123456",
                        "type": "PRODUCT"
                    },
                    "quantity": 1,
                    "unitPrice": 220.14
                }
            ],
            "fiscal_position": "NATIONAL"
        }

        response = self.client.post('/store/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('customer', response.data)
        self.assertIn('email', response.data['customer'])

    def test_create_order_with_missing_customer_data(self):
        data = {
            "customer": {
                "additionalStreet": "",  # Missing required field 'city'
                "companyName": "CLIENTE 1",
                "country": "ES",
                "customerType": "COMPANY",
                "email": "cliente1@cliente1.com",
                "mobilePhone": "123654789",
                "phone": "987456321",
                "postalCode": "98765",
                "street": "Calle Inventada 1",
                "NIF": "01234567L"
            },
            "orderLines": [
                {
                    "orderProduct": {
                        "name": "Producto 1",
                        "sku": "A0123456",
                        "type": "PRODUCT"
                    },
                    "quantity": 1,
                    "unitPrice": 220.14
                }
            ],
            "fiscal_position": "NATIONAL"
        }

        response = self.client.post('/store/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('customer', response.data)
        self.assertIn('city', response.data['customer'])
