from django.shortcuts import render

from products.models import Product


def show_products(request):
    return render(
        request,
        "products/pages/products.html",
        context={"products": Product.objects.all()},
    )


def cart(request):
    return render(request, "products/pages/cart.html")
