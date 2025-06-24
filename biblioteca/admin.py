from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Aluno, Livro, Emprestimo

admin.site.register(Aluno)
admin.site.register(Livro)
admin.site.register(Emprestimo)
