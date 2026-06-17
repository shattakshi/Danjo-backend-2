from django.core.management.base import BaseCommand
from faker import Faker
import random

from products.models import Category, Product
from stores.models import Store, Inventory


class Command(BaseCommand):
    help = "Generate dummy data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write("Creating categories...")

        categories = []

        for i in range(10):
            category, _ = Category.objects.get_or_create(
                name=fake.word().capitalize()
            )

            categories.append(category)

        self.stdout.write("Creating products...")

        products = []

        for i in range(1000):
            product = Product.objects.create(
                title=f"{fake.word().capitalize()} {i}",
                description=fake.sentence(),
                price=random.randint(100, 100000),
                category=random.choice(categories),
            )

            products.append(product)

        self.stdout.write("Creating stores...")

        stores = []

        for i in range(20):
            store = Store.objects.create(
                name=f"{fake.city()} Store",
                location=fake.city(),
            )

            stores.append(store)

        self.stdout.write("Creating inventory...")

        for store in stores:

            selected_products = random.sample(
                products,
                300,
            )

            inventories = []

            for product in selected_products:

                inventories.append(
                    Inventory(
                        store=store,
                        product=product,
                        quantity=random.randint(1, 100),
                    )
                )

            Inventory.objects.bulk_create(
                inventories
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Seed data created successfully!"
            )
        )