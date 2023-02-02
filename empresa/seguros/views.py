from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User, Serviço, Tecnico, Produtos

import random


def index(request):
    return render(request, "seguros/index.html")

def products(request):
    return render(request, "seguros/products.html")

def add(request, produto):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    request.user.seguros.add(produto)
    return HttpResponseRedirect(reverse("myproducts"))
def perfil(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    tecs = Tecnico.objects.all()
    return render(request, "seguros/perfil/perfil.html",{
        "tecs":tecs
    }
    )

def perfil_products(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    seguros = request.user.seguros.all
    
    
    return render(request, "seguros/perfil/my_products.html",{
        "seguros":seguros
    })

def perfil_orders(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    ordens = Serviço.objects.filter(cliente = request.user)
    return render(request, "seguros/perfil/orders.html",{
        "ordens":ordens
    })
    
def create_order(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    seguros = request.user.seguros.all
    usuario = request.user
    tecnico = random.choice(Tecnico.objects.all())
    status = "análise"
    Laudo = ''
    if request.method == "POST":
        title = request.POST["titulo"]
        produto = request.POST["seguro"]
        insurance = Produtos.objects.get(tipo=produto)
        imagem = request.POST["imagem"]
        descrição= request.POST["descrição"]

        job = Serviço(Titulo = title, Descrição=descrição, cliente = usuario, Seguro = insurance, Operador = tecnico, Foto = imagem, Laudo = "", Status = "Em Análise")
        job.save()
        return HttpResponseRedirect(reverse("orders"))

    return render(request, "seguros/perfil/create_order.html",{
        "seguros":seguros
    })

def tecnico(request):
    
    nome = "Ronaldo"
    tec = Tecnico.objects.get(Nome = nome)
    ordens = Serviço.objects.filter(Operador = tec)
    return render(request, "seguros/tecnico.html", {
                "tec":tec,
                "ordens": ordens,
        })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("perfil"))
        else:
            return render(request, "seguros/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "seguros/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name= request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "seguros/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "seguros/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "seguros/register.html")
