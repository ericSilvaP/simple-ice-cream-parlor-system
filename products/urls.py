from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.show_products, name="products"),
    path("carrinho/", views.cart, name="cart"),
    path("carrinho/add/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("carrinho/remover/<int:id>", views.remove_from_cart, name="remove_from_cart"),
    path("carrinho/criarcompra/", views.create_order, name="create_order"),
    path("usuario/cadastro/", views.register_user_view, name="register_user"),
    path(
        "usuario/cadastro/criar/",
        views.register_user_create,
        name="register_user_create",
    ),
    path("usuario/entrar/", views.login_user_view, name="login_user"),
    path("usuario/entrar/criar/", views.login_user_create, name="login_user_create"),
]
