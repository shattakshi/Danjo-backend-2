from django.db.models import Count
from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from stores.models import Inventory

from .models import Order, OrderItem
from .serializers import (
    CreateOrderSerializer,
    OrderSerializer,
)
from .tasks import send_order_confirmation


class CreateOrderView(APIView):

    serializer_class = CreateOrderSerializer

    @transaction.atomic
    def post(self, request):

        serializer = CreateOrderSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        store_id = serializer.validated_data[
            "store_id"
        ]

        items = serializer.validated_data[
            "items"
        ]

        order = Order.objects.create(
            store_id=store_id,
            status=Order.Status.PENDING,
        )

        inventory_items = []

        for item in items:

            inventory = (
                Inventory.objects
                .select_for_update()
                .filter(
                    store_id=store_id,
                    product_id=item["product_id"],
                )
                .first()
            )

            if (
                inventory is None
                or inventory.quantity
                < item["quantity_requested"]
            ):

                order.status = (
                    Order.Status.REJECTED
                )

                order.save()

                return Response(
                    OrderSerializer(order).data,
                    status=status.HTTP_201_CREATED,
                )

            inventory_items.append(
                (inventory, item)
            )

        for inventory, item in inventory_items:

            inventory.quantity -= (
                item["quantity_requested"]
            )

            inventory.save()

            OrderItem.objects.create(
                order=order,
                product_id=item["product_id"],
                quantity_requested=item[
                    "quantity_requested"
                ],
            )

        order.status = (
            Order.Status.CONFIRMED
        )

        order.save()

        # Celery Task
        send_order_confirmation.delay(
            order.id
        )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


class StoreOrdersView(ListAPIView):

    serializer_class = OrderSerializer

    def get_queryset(self):

        store_id = self.kwargs[
            "store_id"
        ]

        return (
            Order.objects
            .filter(
                store_id=store_id
            )
            .annotate(
                total_items=Count("items")
            )
            .prefetch_related(
                "items"
            )
            .order_by(
                "-created_at"
            )
        )