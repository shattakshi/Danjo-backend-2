from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity_requested"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    total_items = serializers.IntegerField(
        read_only=True,
        default=0,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "store",
            "status",
            "created_at",
            "items",
            "total_items",
        ]


class CreateOrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity_requested = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.Serializer):
    store_id = serializers.IntegerField()
    items = CreateOrderItemSerializer(many=True)