from django.shortcuts import render
from usuarios.forms import *
from .models import *
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from .forms import LoginForm
from django.contrib.auth import authenticate
import logging
import googlemaps
from django.contrib import messages
from .forms import *
from geopy.geocoders import Nominatim


# Create your views here.
def registerCliente(request):
    form = ClienteRegistrationForm()

    if request.method == 'POST':
        form = ClienteRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
           
                user = Cliente.objects.create_user(
                    nome = form.cleaned_data['nome'],
                    username = form.cleaned_data['username'],
                    telefone = form.cleaned_data['telefone'],
                    email=form.cleaned_data['email'],
                    foto = form.cleaned_data['foto'],
                    password=form.cleaned_data['password1'],
              
                 
                  
                )
                user.save()

                cep = request.POST.get('cep')
                complemento = request.POST.get('complemento')

                if cep:
                    response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
                    data = response.json()

                    if response.status_code == 200 and not data.get('erro'):
                        estado, _ = Estado.objects.get_or_create(nome=data['uf'])
                        cidade, _ = Cidade.objects.get_or_create(nome=data['localidade'], estado=estado)
                        bairro, _ = Bairro.objects.get_or_create(nome=data['bairro'], cidade=cidade)
                        cep_obj, _ = CEP.objects.get_or_create(codigo=cep)
                        endereco_completo = f"{data['logradouro']}, {data['bairro']}, {data['localidade']}, {data['uf']}, {data['cep']}"
                        latitude, longitude = obter_coordenadas(endereco_completo, "AIzaSyAvXSw3zlzpwUGgH8LOfa4URXceC9LGMI4")

                        endereco, _ = Endereco.objects.get_or_create(
                            rua=data['logradouro'],
                            complemento=complemento,
                            bairro=bairro,
                            cidade=cidade,
                            estado=estado,
                            cep=cep_obj,
                            latitude=latitude,
                            longitude=longitude
                        )

                        user.endereco = endereco
                        user.save()

             
               
               
                    
                messages.success(request, 'Cadastro Realizado com sucesso!')
                return redirect('login')
        else:
            print("Formulário inválido")
            messages.error(request, form.errors)
    
    return render(request, 'core/registroClientes.html', {'form': form})



def obter_coordenadas(endereco_completo, google_maps_api_key):
    gmaps = googlemaps.Client(key=google_maps_api_key)
    geocode_result = gmaps.geocode(endereco_completo)
    
    if geocode_result:
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        return latitude, longitude
    
    return None, None

# Create your views here.
def registerLoja(request):
    categorias = Categoria.objects.all()
    form = LojaRegistrationForm()

    if request.method == 'POST':
        form = LojaRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
           
            user = Loja.objects.create_user(
                nomeLoja = form.cleaned_data['nomeLoja'],
                nome = form.cleaned_data['nome'],
                foto = form.cleaned_data['foto'],
                username = form.cleaned_data['username'],
                telefone = form.cleaned_data['telefone'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                

            
                
                
            )
            cep = request.POST.get('cep')
            complemento = request.POST.get('complemento')

            if cep:
                response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
                data = response.json()

                if response.status_code == 200 and not data.get('erro'):
                    estado, _ = Estado.objects.get_or_create(nome=data['uf'])
                    cidade, _ = Cidade.objects.get_or_create(nome=data['localidade'], estado=estado)
                    bairro, _ = Bairro.objects.get_or_create(nome=data['bairro'], cidade=cidade)
                    cep_obj, _ = CEP.objects.get_or_create(codigo=cep)
                    endereco_completo = f"{data['logradouro']}, {data['bairro']}, {data['localidade']}, {data['uf']}, {data['cep']}"
                    latitude, longitude = obter_coordenadas(endereco_completo, "AIzaSyAvXSw3zlzpwUGgH8LOfa4URXceC9LGMI4")

                    endereco, _ = Endereco.objects.get_or_create(
                        rua=data['logradouro'],
                        complemento=complemento,
                        bairro=bairro,
                        cidade=cidade,
                        estado=estado,
                        cep=cep_obj,
                        latitude=latitude,
                        longitude=longitude
                    )

                    user.endereco = endereco
                    user.save()

                selected_categorias = form.cleaned_data['categorias']

                user.categorias.set(selected_categorias)


             
               
               
                    
                messages.success(request, 'Cadastro Realizado com sucesso!')
                return redirect('login')
                
        else:
            print("Formulário inválido")
            messages.error(request, form.errors)

        
    context = {'categorias':categorias}
    return render(request, 'core/registroEmpresas.html', context)

from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Usuário logado com sucesso!")
            return redirect('home')
        else:
            messages.error(request, "Email ou senha inválidos.")
    else:
        form = LoginForm()
        
        
    return render(request, 'core/login.html')


    
def editar_loja2(request):
    try:
        loja = request.user.loja
    except Loja.DoesNotExist:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

    if request.method == 'POST':
        form = LojaForm(request.POST, request.FILES, instance=loja)
        if form.is_valid():
            form.save()
            # Redirecionar para a página da loja ou alguma página de sucesso
    else:
        form = LojaForm(instance=loja)

    context = { 'loja':loja,
    'form':form,
    }

    return render(request, 'core/editar_loja.html', context)


    
def editar_cliente(request):
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

    if request.method == 'POST':
        form = EditarClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            # Redirecionar para a página da loja ou alguma página de sucesso
    else:
        form = EditarClienteForm(instance=cliente)

    context = { 'cliente':cliente,
    'form':form,
    }

    return render(request, 'core/editar_perfil.html', context)




def editar_loja(request):
    if not request.user.loja:
        return redirect('login')
    user = request.user.loja
    context = {
        'loja':user
    }
    return render(request, 'core/editar_index.html', context)


def catalogo(request):
    if not hasattr(request.user, 'loja'):
        return redirect('login')

    loja = request.user.loja

    categoria_form = CategoriaForm()
    produto_form = ProdutoForm()

    if request.method == 'POST':
        if 'categoria_submit' in request.POST:
            categoria_form = CategoriaForm(request.POST)
            if categoria_form.is_valid():
                nova_categoria = categoria_form.save(commit=False)
                nova_categoria.loja = loja
                nova_categoria.save()

            else:
                print(categoria_form.errors)

        elif 'produto_submit' in request.POST:
            produto_form = ProdutoForm(request.POST, request.FILES)
            if produto_form.is_valid():
                novo_produto = produto_form.save(commit=False)
                categoria_id = request.POST.get('categoriaId')
                novo_produto.categoria = CategoriaProduto.objects.get(id=categoria_id)
                novo_produto.save()

                # Processando múltiplas opções dinâmicas
                opcaoIndex = 0
                while True:
                    opcao_nome = request.POST.get(f'nome_opcao_{opcaoIndex}')
                    if not opcao_nome:
                        break

                    opcao_data = {
                        'nome': opcao_nome,
                        'descricao': request.POST.get(f'descricao_opcao_{opcaoIndex}')
                    }
                    opcao_form = OpcaoForm(opcao_data, {'foto': request.FILES.get(f'foto_opcao_{opcaoIndex}')})
                    if opcao_form.is_valid():
                        nova_opcao = opcao_form.save(commit=False)
                        nova_opcao.produto = novo_produto
                        nova_opcao.save()

                    opcaoIndex += 1
            else:
                print(produto_form.errors)
        return redirect('catalogo')

    context = {
        'categoria_form': categoria_form,
        'produto_form': produto_form,
        'loja': loja,
    }

    return render(request, 'core/catalogo.html', context)

def entrega(request):
    loja = request.user.loja
    
    if request.method == 'POST':
        form = LojaForm(request.POST)

        if 'frete' in request.POST and form.is_valid():
            frete = form.cleaned_data['valor_frete']
            loja.valor_frete = frete
            loja.save()
            return redirect('entrega')

            

        elif 'tempo' in request.POST and form.is_valid():
            tempo = form.cleaned_data['tempo_entrega']
            loja.tempo_entrega = tempo  # Aqui é onde a correção foi feita
            loja.save()
            return redirect('entrega')

        else:
            print(form.errors)

    else:
        form = LojaForm()

    context = {
        'loja': loja,
        'form': form  # Certifique-se de passar o form para o contexto
    }

    return render(request, 'core/entrega.html', context)


def update_capa(request):
    if request.method == 'POST' and 'capa' in request.FILES:
        loja = request.user.loja  # Obtenha o objeto Loja corretamente
        loja.capa = request.FILES['capa']
        loja.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def editar_geral(request):
    loja = request.user.loja
    context = {
        'loja':loja
    }
    return render(request, 'core/editar_geral.html', context)