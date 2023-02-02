from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("products", views.products, name="products"),
    path("perfil/tecnico", views.tecnico, name="tecnico"),
    path("perfil/", views.perfil, name="perfil"),
    path("perfil/orders", views.perfil_orders, name="orders"),
    path("perfil/createorders", views.create_order, name="createorder"),
    path("perfil/products", views.perfil_products, name="myproducts"),
    path("add/<str:produto>",views.add, name="add")
]
