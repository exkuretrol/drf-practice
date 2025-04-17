from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Product
from core.models import User


class ProductRetrieveUpdateDestroyAPIViewTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpassword",
        )
        self.normal_user = User.objects.create_user(
            username="normaluser",
            password="normalpassword",
        )
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=100.0,
            stock=10,
        )
        self.url = reverse("api:product-detail", kwargs={"product_id": self.product.id})

    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_unauthorized_user_update_product(self):
        data = {
            "name": "Updated Product",
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_user_update_product(self):
        self.client.login(username="admin", password="adminpassword")
        data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": "150.00",  # price is defined as a DecimalField
            "stock": 5,
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["name"], "Updated Product")
        self.assertEqual(response.data["description"], "Updated Description")
        self.assertEqual(response.data["price"], "150.00")
        self.assertEqual(response.data["stock"], 5)

    def test_normal_user_update_product(self):
        self.client.login(username="normaluser", password="normalpassword")
        data = {
            "name": "Updated Product",
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_delete_product(self):
        self.client.login(username="admin", password="adminpassword")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_normal_user_delete_product(self):
        self.client.login(username="normaluser", password="normalpassword")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(id=self.product.id).exists())
