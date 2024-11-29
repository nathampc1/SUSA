
from django.contrib import admin
from django.urls import path
from app_SUSA import views

urlpatterns = [
    #rota, view responsável, nome de referência
    path('',views.login, name = 'login'),
    path('cadastro/', views.cadastro, name = 'cadastro'),
    path('clinica/', views.clinica, name='clinica'),
    path('cadastrar/', views.cadastrarUser, name='cadastrar'),
    path('Realizarlogin/', views.RealizarLogin, name='Realizarlogin'),
    path('logout/', views.RealizarLogout, name='logout'),
    path('tutor/', views.tutor, name='tutor'),
    path('msg-inicial/', views.msgInicial, name='msg-inicial'),
    path('servico/', views.cadServico, name='servico'),
    path('cadastrarV/', views.CadastrarServicoV, name='cadastrarV'),
    path('cadastrarC/', views.CadastrarServicoC, name='cadastrarC'),
    path('atualizar/', views.atualizar_servico, name='atualizar_servico'),
    path('atualizarDadosC/', views.atualizarDadosC, name='atualizarDadosC'),
    path('atualizarDadosT/', views.atualizarDadosT, name='atualizarDadosT'),
    path('perfilC/', views.perfilClinica, name='perfilC'),
    path('perfilT/', views.perfilTutor, name='perfilT'),
    path('addPet/', views.addPet, name='addPet'),
    path('meupet/', views.meuPet, name='meupet'),
    path('excluir_pet/<int:pet_id>/', views.excluir_pet, name='excluir_pet'),
    path('perfilpet/<int:pet_id>/', views.perfilPet, name='perfilpet'),
    path('atualizar_pet/<int:pet_id>/', views.atualizar_pet, name='atualizar_pet'),
    path('busca/', views.Busca, name='busca'),
    path('listar_distancia/', views.listar_distancia, name='listar_distancia'),
    path('perfil_clinica/<str:cnpj>/', views.perfil_clinica, name='perfil_clinica'),
    path('realizar_agendamento/<str:cnpj>/', views.realizar_agendamento, name='realizar_agendamento'),
    path('agendamentos/', views.agendamentos, name='agendamentos'),
    path('filtrar_agendamentos/', views.filtrar_agendamentos, name='filtrar_agendamentos'),
    path('excluir/', views.excluir_servico, name='excluir_servico'),
    path('confirmar_consulta/<int:id_agendamento>/', views.confirmar_consulta, name='confirmar_consulta'),
    path('confirmacao/<int:agendamento_id>/', views.confirmacao, name='confirmacao'),
    path('prontuario/<int:agendamento_id>/', views.abrir_prontuario, name='prontuario'),
    path('finalizar_consulta/<int:agendamento_id>/', views.finalizar_consulta, name='finalizar_consulta'),
]
