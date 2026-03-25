from django.urls import path
from . import views

app_name = "products_manager"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("dashboard/hoje/", views.dashboard_today, name="orders_today"),
    path("dashboard/todos/", views.dashboard_all, name="orders_all"),
    path("dashboard/cancelar/<int:pk>/", views.order_cancel, name="order_cancel"),
    path("dashboard/completo/<int:pk>/", views.order_complete, name="order_complete"),
    path("produtos/ver/", views.list_products, name="list_products"),
    path("produtos/editar/<int:pk>/", views.order_complete, name="edit_product"),
]
