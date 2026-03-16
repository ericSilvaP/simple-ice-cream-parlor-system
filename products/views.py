from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from products.models import Category, Order, OrderItem, Product
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from utils.pagination import make_pagination_range
from .forms import LoginUserForm, RegisterUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.paginator import Paginator


def show_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # SEARCH AND FILTER
    search_term = request.GET.get("q", "")
    min_value = request.GET.get("min_value")
    max_value = request.GET.get("max_value")
    categories_filter = [
        categorie.pk
        for categorie in categories
        if request.GET.get(f"category_{categorie.name}") == "on"
    ]
    no_recipes_message = ""

    if search_term:
        products = products.filter(name__icontains=search_term)
        messages.info(request, f'Pesquisa para "{search_term}"')
    if min_value:
        products = products.filter(price__gte=min_value)
    if max_value:
        products = products.filter(price__lte=max_value)
    if categories_filter:
        products = products.filter(category__in=categories_filter)

    # PAGINATION
    try:
        current_page = int(request.GET.get("page", 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(products, 9)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(paginator.page_range, 5, current_page)

    if not products:
        no_recipes_message = "Nenhum produto foi encontrado"

    return render(
        request,
        "products/pages/products.html",
        context={
            "products": page_obj,
            "no_recipes_message": no_recipes_message,
            "pagination_range": pagination_range,
            "categories": categories,
        },
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
@login_required(login_url="products:login_user")
def create_order(request: HttpRequest):
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

    order = Order.objects.create(total_value=total_value, user=request.user)
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
            "submit_button_text": "Cadastrar",
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
            "submit_button_text": "Entrar",
            "show_register": True,
            "login_title_text": "Entrar",
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


@login_required(login_url="products:login_user", redirect_field_name="next")
@require_POST
def logout_view(request):
    logout(request)
    return redirect("products:login_user")


@login_required(login_url="products:login_user")
def orders_view(request):
    orders = Order.objects.filter(user=request.user).annotate(
        items_number=Sum("items__quantity")
    )

    return render(request, "products/pages/orders.html", context={"orders": orders})
