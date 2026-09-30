from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cadastrar/', views.cadastrar_material, name='cadastrar_material'),
    path('editar/<int:pk>/', views.editar_material, name='editar_material'),
    path('excluir/<int:pk>/', views.excluir_material, name='excluir_material'),
    path('materiais/', views.listar_materiais, name='listar_materiais'),

    path('relatorio/pdf/', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
    path('entrada-validade/<int:pk>/', views.entrada_validade, name='entrada_validade'),
]