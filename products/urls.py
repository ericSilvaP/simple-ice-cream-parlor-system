from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.show_products, name="products"),
    path("carrinho/", views.cart, name="cart"),
    path("carrinho/add/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("carrinho/remover/<int:id>", views.remove_from_cart, name="remove_from_cart"),
    path("carrinho/criarcompra/", views.create_order, name="create_order"),
]
