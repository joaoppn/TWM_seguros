from django.contrib.auth.models import AbstractUser
from django.db import models

class Produtos(models.Model):
    tipo = models.CharField(max_length=64, primary_key=True)
    def __str__(self):
        return f"{self.tipo}"

class User(AbstractUser):
    seguros = models.ManyToManyField(Produtos)
    pass
    def __str__(self):
        return f"{self.id}"

class Tecnico(models.Model):
    Nome = models.CharField(max_length=64, primary_key='True')
    Email = models.CharField(max_length=128)
    Password = models.CharField(max_length=64)
    Status = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.Nome}"

class Serviço(models.Model):
    Titulo = models.CharField(max_length=64, primary_key='True')
    Descrição = models.CharField(max_length=256)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    Seguro = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    Operador = models.ForeignKey(Tecnico, on_delete=models.CASCADE)
    Foto = models.ImageField(upload_to='fotos/laudos/', default="NULL")
    Laudo = models.CharField(max_length=256)
    Status = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.Titulo}: {self.Seguro} do {self.cliente.get_full_name}"