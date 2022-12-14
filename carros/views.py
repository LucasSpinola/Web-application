from django.shortcuts import render, redirect
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Carro, Categoria, Emprestimo
from .forms import CadastroCarro, CategoriaCarro
from usuarios.models import Usuario
from datetime import datetime, date
from django.db.models import Q

def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id=request.session['usuario'])
        status_categoria = request.GET.get('cadastro_categoria')
        carros = Carro.objects.filter(usuario=usuario)
        total_carros = carros.count()
        forms = CadastroCarro()
        forms.fields['usuario'].initial = request.session['usuario']
        forms.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)
        forms_categoria = CategoriaCarro()
        img = Carro.objects.filter(usuario=usuario).filter(img__isnull=False)
        usuarios = Usuario.objects.all()
        carros_emprestar = Carro.objects.filter(usuario=usuario).filter(alugado=False)
        carros_emprestados = Carro.objects.filter(usuario=usuario).filter(alugado=True)
        
        return render(request, 'home.html', {'carros': carros,
                                             'usuario_logado': request.session.get('usuario'),
                                             'forms': forms,
                                             'status_categoria': status_categoria,
                                             'forms_categoria': forms_categoria,
                                             'usuarios': usuarios,
                                             'carros_emprestar': carros_emprestar,
                                             'total_carros': total_carros,
                                             'carros_emprestados': carros_emprestados,
                                             'img': img})
    else:
        return redirect('/auth/login/?status=2')
    
def ver_carros(request, id):
    if request.session.get('usuario'):
        carro = Carro.objects.get(id=id)
        if request.session.get('usuario') == carro.usuario_id:
            usuario = Usuario.objects.get(id=request.session['usuario'])
            categoria_carro = Categoria.objects.filter(usuario = request.session.get('usuario'))
            emprestimos = Emprestimo.objects.filter(carro = carro)
            forms = CadastroCarro()
            forms.fields['usuario'].initial = request.session['usuario']	
            forms_categoria = CategoriaCarro()
            usuarios = Usuario.objects.all()
            carros_emprestar = Carro.objects.filter(usuario=usuario).filter(alugado=False)
            carros_emprestados = Carro.objects.filter(usuario=usuario).filter(alugado=True)
        
        return render(request, 'ver_carro.html', {'carro': carro,
                                                  'categoria_carro': categoria_carro,
                                                  'emprestimos': emprestimos,
                                                  'usuario_logado': request.session.get('usuario'),
                                                  'forms': forms,
                                                  'id_carro': id,
                                                  'forms_categoria': forms_categoria,
                                                  'usuarios': usuarios,
                                                  'carros_emprestar': carros_emprestar,
                                                  'carros_emprestados': carros_emprestados})
    else: 
        return redirect('/auth/login/?status=2')


def cadastrar_carro(request):
    if request.method == 'POST':
        forms = CadastroCarro(request.POST)
        
        if forms.is_valid():
            forms.save()
            return redirect('/carros/home')
        else:
            return HttpResponse('DADOS INVALIDOS')
        

def excluir_carro(request, id):
    carros = Carro.objects.get(id=id).delete()
    return redirect('/carros/home')

def cadastrar_categoria(request):
    forms = CategoriaCarro(request.POST)
    nome = forms.data['nome']
    descricao = forms.data['descricao']
    id_usuario = request.POST.get('usuario')
    if int(id_usuario) == int(request.session.get('usuario')):
        user = Usuario.objects.get(id=id_usuario)
        categoria = Categoria(nome=nome, descricao=descricao, usuario=user)
        categoria.save()
        return redirect('/carros/home?cadastro_categoria=1')
    else:
        return redirect('/auth/login/?status=5')

def cadastrar_emprestimos(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')
        nome_emprestado_anonimo = request.POST.get('nome_emprestado_anonimo')
        carro_emprestado = request.POST.get('carro_emprestado')
        if nome_emprestado_anonimo:
            emprestimos = Emprestimo(nome_emprestado_anonimo = nome_emprestado_anonimo,
                                    carro_id = carro_emprestado)
        else:
            emprestimos = Emprestimo(nome_emprestado_id = nome_emprestado,
                                     carro_id = carro_emprestado)        
        
        emprestimos = Emprestimo(nome_emprestado_id = nome_emprestado ,
                                 carro_id = carro_emprestado)
        emprestimos.save()
        
        carro = Carro.objects.get(id = carro_emprestado)
        carro.alugado = True
        carro.save()
        return redirect('/carros/home')
    
def devolver_carro(request):
    id = request.POST.get('id_carro_devolver')
    carro_devolver = Carro.objects.get(id=id)
    alugado_devolver = Emprestimo.objects.get(Q(carro= carro_devolver) & Q(data_devolucao=None))
    alugado_devolver.data_devolucao = datetime.now()
    alugado_devolver.save()
    carro_devolver.alugado = False
    carro_devolver.save()
    return redirect('/carros/home')

def editar_carro(request):
    carro_id = request.POST.get('carro_id')
    nome_carro = request.POST.get('nome_carro')
    marca = request.POST.get('marca')
    ano = request.POST.get('ano')
    cor = request.POST.get('cor')
    preco = request.POST.get('preco')
    categoria_id = request.POST.get('categoria_id')
    categoria = Categoria.objects.get(id=categoria_id)
    carros = Carro.objects.get(id=carro_id)
    if carros.usuario.id == request.session['usuario']:
        carros.nome = nome_carro
        carros.marca = marca
        carros.ano = ano
        carros.cor = cor
        carros.preco = preco
        carros.categoria = categoria
        carros.save()
    
        return redirect(f'/carros/ver_carro/{carro_id}')
    else:
        return redirect('/auth/sair/')
    

def seus_emprestimo(request):
    usuario = Usuario.objects.get(id=request.session['usuario'])
    emprestimos = Emprestimo.objects.filter(nome_emprestado=usuario)
    
    
    return render(request, 'seus_emprestimos.html', {'usuario_logado': request.session['usuario'],
                                                     'emprestimos': emprestimos})
    
 
def processa_avaliacao(request):
    id_alugado = request.POST.get('id_alugado')
    opcoes = request.POST.get('opcoes')
    id_carro = request.POST.get('id_carro')
    
    emprestimo=Emprestimo.objects.get(id = id_alugado)
    if emprestimo.carro.usuario.id == request.session['usuario']:
        emprestimo.avaliacao = opcoes
        emprestimo.save()
        return redirect(f'/carros/ver_carro/{id_carro}')
    else:
        return redirect('/auth/sair/')