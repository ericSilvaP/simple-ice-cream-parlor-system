from django.shortcuts import render, redirect, get_object_or_404
from products.forms import LoginUserForm
from products.models import Order
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages


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
    orders = Order.objects.filter(created_at__date=today, status="pending")
    return render(
        request,
        "products_manager/pages/orders_today.html",
        context={"pending_orders": orders},
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
