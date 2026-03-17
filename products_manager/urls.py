from django.urls import path
from . import views

app_name = "products_manager"

urlpatterns = [
    path("", views.login, name="login"),
]
