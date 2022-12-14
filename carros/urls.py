from django.urls import path
from . import  views

urlpatterns = [
    path('home/', views.home, name = 'home'),
    path('ver_carro/<int:id>', views.ver_carros, name = 'ver_carros'),
    path('cadastrar_carro/', views.cadastrar_carro, name = 'cadastrar_carro'),
    path('excluir_carro/<int:id>', views.excluir_carro, name = 'excluir_carro'),
    path('cadastrar_categoria', views.cadastrar_categoria, name = 'cadastrar_categoria'),
    path('cadastrar_emprestimos', views.cadastrar_emprestimos, name = 'cadastrar_emprestimos'),
    path('devolver_carro', views.devolver_carro, name = 'devolver_carro'),
    path('editar_carro', views.editar_carro, name ='editar_carro'),
    path('seus_emprestimo', views.seus_emprestimo, name = 'seus_emprestimo'),
    path('processa_avaliacao', views.processa_avaliacao, name = 'processa_avaliacao'),
]