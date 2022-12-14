from django.db import models
from datetime import date
from usuarios.models import Usuario
import datetime

class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.nome


class Carro(models.Model):
    img = models.ImageField(upload_to='capa_carro', blank=True, null=True)
    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    ano = models.IntegerField()
    cor = models.CharField(max_length=15)
    preco = models.FloatField()
    data_cadastro = models.DateField(default= date.today)
    alugado = models.BooleanField(default=False, blank=True)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.SET_NULL)
    usuario = models.ForeignKey(Usuario, null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.nome

class Emprestimo(models.Model):
    choices = (
        ('Péssimo', 'Péssimo'),
        ('Bom', 'Bom'),
        ('Ótimo', 'Ótimo'),
    )
    nome_emprestado = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True, null=True)
    nome_emprestado_anonimo = models.CharField(max_length=30, blank=True, null=True)
    data_emprestado = models.DateTimeField(default=datetime.datetime.now())
    data_devolucao = models.DateTimeField(blank=True, null=True)
    carro = models.ForeignKey(Carro, on_delete=models.DO_NOTHING)
    avaliacao = models.CharField(max_length=7, choices=choices, null=True, blank=True)
    
    def __str__(self):
        return f'{self.nome_emprestado} | {self.carro}'
    