from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product


def show_products(request):
    return render(
        request,
        "products/pages/products.html",
        context={"products": Product.objects.all()},
    )


def add_to_cart(request, id):
    product = Product.objects.get(pk=id)
    cart = request.session.get("cart", {})
    pk = str(product.pk)
    messages.success(request, "Produto adicionado ao carrinho!")
    if pk not in cart:
        request.session["cart"].update({str(pk): 1})

    return redirect("products:products")


def cart(request):
    return render(request, "products/pages/cart.html")
