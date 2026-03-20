from django.shortcuts import render
from products.forms import LoginUserForm
from products.models import Order
from django.utils import timezone


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
    orders = Order.objects.filter(created_at__date=today)
    return render(
        request,
        "products_manager/pages/orders_today.html",
        context={"pending_orders": orders},
    )
