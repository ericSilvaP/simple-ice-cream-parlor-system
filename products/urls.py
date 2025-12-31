from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.show_products, name="products"),
    path("carrinho/", views.cart, name="cart"),
    path("add_to_cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:id>", views.remove_from_cart, name="remove_from_cart"),
]
