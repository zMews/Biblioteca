from django.db import models

# Create your models here.
from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.IntegerField(primary_key=True)
    email = models.EmailField()
    curso = models.CharField(max_length=100)
    data_nascimento = models.DateField()

    def __str__(self):
        return f"{self.nome} ({self.matricula})"


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    editora = models.CharField(max_length=100)
    isbn = models.BigIntegerField(primary_key=True)
    quantidade_disponivel = models.SmallIntegerField()

    def __str__(self):
        return f"{self.titulo} - {self.autor}"


class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.SET_NULL, null=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.SET_NULL, null=True)
    data_emprestimo = models.DateField()
    data_devolucao = models.DateField()
    data_devolvido = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.aluno} -> {self.livro}"
