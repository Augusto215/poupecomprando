from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('lojas/', listar_lojas, name='listar_lojas'),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
    path('payment/', comprar_credito, name='payment'),
    path('loja/', loja, name='loja1'),
    path('credito_sucesso/', credito_sucesso, name='credito_sucesso'),
    path('lojas_proximas/', loja, name='loja'),
    path('loja/<int:loja_id>/', perfil_loja, name='perfil_loja'),
    path('set_location/', set_location, name='set_location'),




    





    

    # Aqui estamos definindo a rota para a sua view home
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)