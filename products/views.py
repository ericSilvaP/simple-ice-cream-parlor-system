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
    cart = request.session.get("cart")
    if not cart:
        cart = {}
    messages.success(request, "Produto adicionado ao carrinho!")
    cart.update({str(product.pk): 1})
    request.session["cart"] = cart

    return redirect("products:products")


def cart(request):
    order = request.session.get("cart")
    if not order:
        order = {}
    products = [Product.objects.get(id=id) for id in order.keys()]
    order = list(zip(products, order.values()))
    return render(request, "products/pages/cart.html", context={"order": order})
