import uuid

from django.db import models

from core.models import User


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        CONFIRMED = "Confirmed"
        CANCELLED = "Cancelled"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, default=StatusChoices.PENDING, choices=StatusChoices.choices
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    products = models.ManyToManyField(
        "Product", through="OrderItem", related_name="orders"
    )

    def __str__(self):
        return f"Order {self.uuid} by {self.user.username}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="produces/", null=True)

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.uuid}"
