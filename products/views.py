import re
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from products.models import Order, OrderItem, Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def show_products(request):
    return render(
        request,
        "products/pages/products.html",
        context={"products": Product.objects.all()},
    )


@require_POST
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


@require_POST
def remove_from_cart(request, id):
    cart = request.session.get("cart", {})
    product_id = str(id)
    if product_id in cart:
        del cart[product_id]
        request.session["cart"] = cart

    return JsonResponse({"success": True})


@require_POST
def create_order(request):
    quantities = {
        x[-1]: int(y) for x, y in request.POST.items() if x.startswith("quantity")
    }
    del request.session["cart"]
    products = [Product.objects.get(id=id) for id in quantities.keys()]
    total_value = sum(
        [
            float(product.price) * quantities.get(str(product.pk), 1)
            for product in products
        ]
    )

    order = Order.objects.create(total_value=total_value)
    for product in products:
        product_instance = get_object_or_404(Product, pk=product.pk)
        OrderItem.objects.create(
            order=order,
            product=product_instance,
            quantity=quantities.get(str(product.pk), 1),
        )
    messages.success(request, "Compra realizada com sucesso!")
    return redirect("products:products")
