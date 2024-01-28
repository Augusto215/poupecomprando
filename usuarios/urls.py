from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('registrarCliente/', registerCliente, name='registerCliente'),
    path('registrarLoja/', registerLoja, name='registerLoja'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('entrar/', user_login, name='login'),
    path('editar_loja/', editar_loja, name='editar_loja'),
    path('editar_cliente/', editar_cliente, name='editar_cliente'),
    path('editar_catalogo/', catalogo, name='catalogo'),
    path('alterar_entrega/', entrega, name='entrega'),
    path('update_capa/', update_capa, name='update_capa'),
    path('editar_geral/', editar_geral, name='editar_geral')





]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)