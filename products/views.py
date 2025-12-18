from django.shortcuts import render


def show_products(request):
    return render(request, "products/pages/products.html")
