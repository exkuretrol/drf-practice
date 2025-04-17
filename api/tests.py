from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from api.models import Order
from core.models import User


class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1", password="password")
        user2 = User.objects.create(username="user2", password="password")
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)

    def test_user_orders_endpoint_only_retrieve_user_orders(self):
        user1 = User.objects.get(username="user1")
        self.client.force_login(user1)

        response = self.client.get(reverse("api:user-order-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        orders = response.json()
        self.assertTrue(all(order["user"] == user1.id for order in orders))
        self.client.logout()

    def test_unauthenticated_user_cannot_access_user_orders_endpoint(self):
        response = self.client.get(reverse("api:user-order-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
