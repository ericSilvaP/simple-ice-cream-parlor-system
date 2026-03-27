from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from products.forms import LoginUserForm
from products.models import Category, Order, Product
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator

from products_manager.forms import ProductForm
from utils.filter import filter_orders, filter_products
from utils.pagination import make_pagination_range
from django.db.models import Q

from utils.pagination_url import (
    create_orders_pagination_url,
    create_products_pagination_url,
)


def login(request):
    form = LoginUserForm()
    return render(
        request,
        "products_manager/pages/login.html",
        context={
            "form": form,
            "submit_button_text": "Entrar",
            "login_title_text": "Administração",
            "hidden_sidebar": True,
        },
    )


def dashboard_today(request):
    today = timezone.localdate()
    pending_orders = Order.objects.filter(created_at__date=today, status="pending")
    other_orders = Order.objects.filter(
        Q(created_at__date=today) & ~Q(status="pending")
    )
    return render(
        request,
        "products_manager/pages/orders_today.html",
        context={
            "pending_orders": pending_orders,
            "other_orders": other_orders,
        },
    )


def dashboard_all(request):
    orders = Order.objects.all()
    categories = Category.objects.all()

    # SEARCH AND FILTER
    search_term = request.GET.get("q", "")
    min_value = request.GET.get("min_value", 0)
    max_value = request.GET.get("max_value", 0)
    status_list = ["Completo", "Cancelado", "Pendente"]

    status_search_list = []
    for status in status_list:
        if status == "Completo" and request.GET.get(status):
            status_search_list.append(status)
        if status == "Cancelado" and request.GET.get(status):
            status_search_list.append(status)
        if status == "Pendente" and request.GET.get(status):
            status_search_list.append(status)

    orders, search_term = filter_orders(
        request, orders, search_term, min_value, max_value, status_list
    )

    if search_term:
        messages.info(request, f'Pesquisa para "{search_term}"')
    elif not orders:
        messages.error(request, "Nenhuma receita encontrada")
        orders = Order.objects.all()

    # PAGINATION
    try:
        current_page = int(request.GET.get("page", 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(orders, 30)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(paginator.page_range, 5, current_page)
    pagination_url = create_orders_pagination_url(
        search_term, min_value, max_value, status_search_list
    )
    return render(
        request,
        "products_manager/pages/orders_all.html",
        context={
            "all_orders": page_obj,
            "page_obj": page_obj,
            "categories": categories,
            "modal_path": "products_manager/partials/filter-modal.html",
            "status_list": status_list,
            "pagination_range": pagination_range,
            "pagination_url": pagination_url,
        },
    )


@require_POST
def order_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = "complete"
    order.save()
    messages.success(request, f"Pedido {order.pk} completo")
    return redirect("products_manager:orders_today")


@require_POST
def order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = "canceled"
    order.save()
    messages.error(request, f"Pedido {order.pk} cancelado")
    return redirect("products_manager:orders_today")


def list_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # SEARCH AND FILTER
    search_term = request.GET.get("q", "")
    min_value = request.GET.get("min_value", 0)
    max_value = request.GET.get("max_value", 0)
    categories_filter = [
        categorie
        for categorie in categories
        if request.GET.get(f"category_{categorie.name}") == "on"
    ]

    products, search_term = filter_products(
        products, search_term, min_value, max_value, categories_filter
    )

    if search_term:
        messages.info(request, f'Pesquisa para "{search_term}"')
    elif not products:
        messages.error(request, "Nenhum produto encontrado")
        products = Product.objects.all()

    # PAGINATION
    try:
        current_page = int(request.GET.get("page", 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(products, 30)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(paginator.page_range, 5, current_page)

    pagination_url = create_products_pagination_url(
        search_term,
        min_value,
        max_value,
        [category.name for category in categories_filter],
    )
    return render(
        request,
        "products_manager/pages/list-products.html",
        context={
            "page_obj": page_obj,
            "categories": categories,
            "hidden_add_to_cart_button": True,
            "pagination_range": pagination_range,
            "modal_path": "products/partials/filter-modal.html",
            "pagination_url": pagination_url,
        },
    )


def edit_product(request, pk):
    POST = request.session.get("product_form_data", "")
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(POST or None, instance=product)
    return render(
        request,
        "products_manager/pages/edit-product.html",
        context={
            "form": form,
            "product_id": pk,
            "submit_button_text": "Salvar",
            "form_action": reverse("products_manager:save_product", kwargs={"pk": pk}),
        },
    )


@require_POST
def save_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(
        request.POST or None,
        files=request.FILES or None,
        instance=product,
    )
    request.session["product_form_data"] = request.POST
    if form.is_valid():
        form.save()
        messages.success(request, "Produto editado com sucesso")
        del request.session["product_form_data"]

    return redirect("products_manager:edit_product", pk=pk)


def create_product(request):
    POST = request.session.get("product_form_data", "")
    form = ProductForm(POST or None)
    return render(
        request,
        "products_manager/pages/create-product.html",
        context={
            "form": form,
            "submit_button_text": "Salvar",
            "form_action": reverse("products_manager:create_product_save"),
        },
    )


@require_POST
def create_product_save(request):
    form = ProductForm(
        request.POST or None,
        files=request.FILES or None,
    )
    request.session["product_form_data"] = request.POST
    if form.is_valid():
        new_product = form.save()
        messages.success(request, "Produto criado com sucesso")
        del request.session["product_form_data"]
    else:
        return redirect("products_manager:create_product")

    return redirect("products_manager:edit_product", pk=new_product.pk)
