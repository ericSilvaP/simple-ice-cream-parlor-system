from django.urls import path
from . import views

app_name = "products_manager"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("dashboard/hoje/", views.dashboard_today, name="orders_today"),
    path("dashboard/todos/", views.dashboard_today, name="orders_all"),
    path("dashboard/todos/<int:pk>", views.dashboard_today, name="order_cancel"),
    path("dashboard/todos/<int:pk>", views.dashboard_today, name="order_complete"),
]
