from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from products.models import Order, OrderItem, Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import LoginUserForm, RegisterUserForm
from django.contrib.auth import authenticate, login


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


def register_user_view(request):
    form = RegisterUserForm(request.session.get("register_user_form_data"))
    form_action = reverse("products:register_user_create")
    return render(
        request,
        "products/pages/register-user.html",
        context={
            "form": form,
            "form_action": form_action,
        },
    )


@require_POST
def register_user_create(request):
    POST = request.POST
    request.session["register_user_form_data"] = POST
    form = RegisterUserForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        del request.session["register_user_form_data"]
        messages.success(request, "Usuário criado com sucesso!")
        return redirect("products:login_user")

    return redirect("products:register_user")


def login_user_view(request):
    form = LoginUserForm()
    form_action = reverse("products:login_user_create")
    return render(
        request,
        "products/pages/login-user.html",
        context={
            "form": form,
            "form_action": form_action,
        },
    )


@require_POST
def login_user_create(request):
    form = LoginUserForm(request.POST)
    if form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password"),
        )
        if user is not None:
            login(request, user)
            messages.success(request, f"Seja bem-vindo(a), {user.get_username()}!")
            return redirect(reverse("products:products"))

    return redirect("products:login_user")
