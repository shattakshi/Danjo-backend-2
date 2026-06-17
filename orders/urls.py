from django.urls import path
from .views import CreateOrderView, StoreOrdersView

urlpatterns = [
    path(
        "orders/",
        CreateOrderView.as_view(),
        name="create-order",
    ),

    path(
        "stores/<int:store_id>/orders/",
        StoreOrdersView.as_view(),
        name="store-orders",
    ),
]