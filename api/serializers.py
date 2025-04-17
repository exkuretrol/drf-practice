from django.db import transaction
from rest_framework import serializers

from .models import Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True, read_only=True)
    counts = serializers.IntegerField()
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = OrderItem
        fields = (
            "product_name",
            "product_price",
            "quantity",
        )


class OrderSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = Order
        fields = (
            "uuid",
            "created_at",
            "status",
            "items",
            "total_price",
        )

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = (
                "product",
                "quantity",
            )

    uuid = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop("items", None)
        with transaction.atomic():
            order = super().update(instance, validated_data)

            if order_items_data is not None:
                order.items.all().delete()

                for order_item in order_items_data:
                    OrderItem.objects.create(order=order, **order_item)

        return order

    def create(self, validated_data):
        order_items_data = validated_data.pop("items", None)

        if order_items_data is None or not order_items_data:
            raise serializers.ValidationError(detail="Order items are required.")

        with transaction.atomic():
            order = Order.objects.create(
                status=Order.StatusChoices.PENDING, **validated_data
            )

            for order_item in order_items_data:
                OrderItem.objects.create(order=order, **order_item)

        return order

    class Meta:
        model = Order
        fields = (
            "uuid",
            "user",
            "status",
            "items",
            "created_at",
        )

        extra_kwargs = {
            "user": {
                "read_only": True,
            },
        }
