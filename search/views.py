import redis

from django.db.models import Q, F, Count
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from products.models import Product
from .serializers import ProductSearchSerializer


redis_client = redis.Redis(
    host="redis",
    port=6379,
    db=0,
    decode_responses=True,
)


class ProductPagination(PageNumberPagination):
    page_size = 10


class ProductSearchView(ListAPIView):
    serializer_class = ProductSearchSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.select_related("category")

        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
            )

        category = self.request.GET.get("category")

        if category:
            queryset = queryset.filter(
                category__name__iexact=category
            )

        min_price = self.request.GET.get("min_price")

        if min_price:
            queryset = queryset.filter(
                price__gte=min_price
            )

        max_price = self.request.GET.get("max_price")

        if max_price:
            queryset = queryset.filter(
                price__lte=max_price
            )

        store_id = self.request.GET.get("store_id")

        if store_id:
            queryset = queryset.filter(
                inventories__store_id=store_id
            )

        in_stock = self.request.GET.get("in_stock")

        if in_stock == "true":
            queryset = queryset.filter(
                inventories__quantity__gt=0
            )

        sort = self.request.GET.get("sort")

        if sort == "price":
            queryset = queryset.order_by("price")

        elif sort == "newest":
            queryset = queryset.order_by("-created_at")

        elif sort == "relevance" and query:
            queryset = queryset.annotate(
                relevance=Count("id")
            ).order_by("-relevance")

        return queryset.annotate(
            category_name=F("category__name")
        ).values(
            "id",
            "title",
            "price",
            "category_name",
        ).distinct()


class ProductSuggestView(APIView):

    def get(self, request):

        ip = request.META.get("REMOTE_ADDR")

        key = f"autocomplete:{ip}"

        count = redis_client.get(key)

        if count and int(count) >= 20:
            return Response(
                {
                    "error": "Rate limit exceeded. Try again later."
                },
                status=429,
            )

        pipe = redis_client.pipeline()

        pipe.incr(key)
        pipe.expire(key, 60)

        pipe.execute()

        query = request.GET.get("q", "").strip()

        if len(query) < 3:
            return Response(
                {
                    "error": "Minimum 3 characters required"
                },
                status=400,
            )

        prefix_matches = Product.objects.filter(
            title__istartswith=query
        ).values_list(
            "title",
            flat=True,
        )[:10]

        other_matches = Product.objects.filter(
            title__icontains=query
        ).exclude(
            title__istartswith=query
        ).values_list(
            "title",
            flat=True,
        )[:10]

        suggestions = list(prefix_matches) + list(other_matches)

        return Response(suggestions[:10])