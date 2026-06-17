from django.test import TestCase

from orders.models import Order
from products.models import Category, Product
from stores.models import Store


class OrderModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics"
        )

        self.product = Product.objects.create(
            title="Laptop",
            price=50000,
            category=self.category
        )

        self.store = Store.objects.create(
            name="Store A",
            location="Noida"
        )

    def test_order_creation(self):
        order = Order.objects.create(
            store=self.store,
            status=Order.Status.PENDING
        )

        self.assertEqual(
            order.status,
            Order.Status.PENDING
        )

    def test_order_string_representation(self):
        order = Order.objects.create(
            store=self.store
        )

        self.assertTrue(
            str(order).startswith("Order")
        )

    def test_order_store_relation(self):
        order = Order.objects.create(
            store=self.store
        )

        self.assertEqual(
            order.store.name,
            "Store A"
        )