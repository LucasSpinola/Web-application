from django.urls import path
from . import  views

urlpatterns = [
    path('home/', views.home, name = 'home'),
    path('ver_carro/<int:id>', views.ver_carros, name = 'ver_carros'),
    path('cadastrar_carro/', views.cadastrar_carro, name = 'cadastrar_carro'),
    path('excluir_carro/<int:id>', views.excluir_carro, name = 'excluir_carro'),
    path('cadastrar_categoria', views.cadastrar_categoria, name = 'cadastrar_categoria'),
    path('cadastrar_emprestimos', views.cadastrar_emprestimos, name = 'cadastrar_emprestimos'),
    path('devolver_carros', views.devolver_carros, name = 'devolver_carros'),
    path('editar_carro', views.editar_carro, name ='editar_carro'),
]