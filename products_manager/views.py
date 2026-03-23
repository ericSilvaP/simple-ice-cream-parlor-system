from django.shortcuts import render, redirect, get_object_or_404
from products.forms import LoginUserForm
from products.models import Category, Order
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator

from utils.pagination import make_pagination_range
from django.db.models import Q


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
    min_value = request.GET.get("min_value")
    max_value = request.GET.get("max_value")
    status_list = ["Completo", "Cancelado", "Pendente"]

    if search_term:
        if str(search_term).isdigit():
            orders = orders.filter(pk__icontains=search_term)
        else:
            orders = orders.filter(user__username__icontains=search_term)

        if orders:
            messages.info(request, f'Pesquisa para "{search_term}"')
        else:
            orders = Order.objects.all()
    if min_value:
        orders = orders.filter(price__gte=min_value)
    if max_value:
        orders = orders.filter(price__lte=max_value)
    for status in status_list:
        status_search = ""
        if status == "Completo" and request.GET.get(status):
            status_search = "complete"
        if status == "Cancelado" and request.GET.get(status):
            status_search = "canceled"
        if status == "Pendente" and request.GET.get(status):
            status_search = "pending"

        if status_search:
            orders = orders.filter(status=status_search)

    # PAGINATION
    try:
        current_page = int(request.GET.get("page", 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(orders, 30)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(paginator.page_range, 5, current_page)

    return render(
        request,
        "products_manager/pages/orders_all.html",
        context={
            "pending_orders": page_obj,
            "page_obj": page_obj,
            "categories": categories,
            "modal_path": "products_manager/partials/filter-modal.html",
            "status_list": status_list,
            "pagination_range": pagination_range,
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
