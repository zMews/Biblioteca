from django.urls import path
from . import views

urlpatterns = [
    path('alunos/', views.aluno_list, name='aluno_list'),
    path('alunos/novo/', views.aluno_create, name='aluno_create'),
    path('alunos/<int:pk>/editar/', views.aluno_update, name='aluno_update'),
    path('alunos/<int:pk>/deletar/', views.aluno_delete, name='aluno_delete'),
    path('livros/', views.livro_list, name='livro_list'),
    path('livros/novo/', views.livro_create, name='livro_create'),
    path('livros/<int:pk>/editar/', views.livro_update, name='livro_update'),
    path('livros/<int:pk>/deletar/', views.livro_delete, name='livro_delete'),
    path('emprestimos/', views.emprestimo_list, name='emprestimo_list'),
    path('emprestimos/novo/', views.emprestimo_create, name='emprestimo_create'),
    path('emprestimos/<int:pk>/devolver/', views.emprestimo_devolver, name='emprestimo_devolver'),
    path('', views.home, name='home'),
    path('busca/', views.busca, name='busca'),
]
