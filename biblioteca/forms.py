from django import forms
from .models import Aluno
from .models import Livro
from .models import Emprestimo
from django.core.exceptions import ValidationError
from datetime import date
import re

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'matricula', 'email', 'curso', 'data_nascimento']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome completo'}),
            'matricula': forms.NumberInput(attrs={'placeholder': 'Matrícula'}),
            'email': forms.EmailInput(attrs={'placeholder': 'exemplo@email.com'}),
            'curso': forms.TextInput(attrs={'placeholder': 'Curso'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        labels = {
            'nome': 'Nome completo',
            'matricula': 'Matrícula',
            'email': 'E-mail institucional',
            'curso': 'Curso',
            'data_nascimento': 'Data de nascimento',
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if not re.fullmatch(r'[A-Za-zÀ-ÿ\s]+', nome):
            raise forms.ValidationError("O nome deve conter apenas letras e espaços.")
        return nome

    def clean_curso(self):
        curso = self.cleaned_data.get('curso')
        if not re.fullmatch(r'[A-Za-zÀ-ÿ\s]+', curso):
            raise forms.ValidationError("O curso deve conter apenas letras e espaços.")
        return curso

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula')
        if matricula is not None and matricula <= 0:
            raise forms.ValidationError("A matrícula deve ser um número positivo.")
        return matricula

    def clean_data_nascimento(self):
        nascimento = self.cleaned_data.get('data_nascimento')
        if nascimento:
            hoje = date.today()
            idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
            if idade > 150:
                raise forms.ValidationError("A idade máxima permitida é de 150 anos.")
        return nascimento


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora', 'isbn', 'quantidade_disponivel']

        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título do livro'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Nome do autor'}),
            'editora': forms.TextInput(attrs={'placeholder': 'Nome da editora'}),
            'isbn': forms.NumberInput(attrs={'placeholder': 'Código ISBN'}),
            'quantidade_disponivel': forms.NumberInput(attrs={'min': 0}),
        }

        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'editora': 'Editora',
            'isbn': 'ISBN',
            'quantidade_disponivel': 'Exemplares disponíveis',
        }

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['aluno', 'livro', 'data_emprestimo', 'data_devolucao']

        widgets = {
            'data_emprestimo': forms.DateInput(attrs={'type': 'date'}),
            'data_devolucao': forms.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            'aluno': 'Aluno',
            'livro': 'Livro',
            'data_emprestimo': 'Data do empréstimo',
            'data_devolucao': 'Data prevista para devolução',
        }


#overdrive clean
    def clean(self):
        cleaned_data = super().clean()
        livro = cleaned_data.get('livro')
        data_emprestimo = cleaned_data.get('data_emprestimo')
        data_devolucao = cleaned_data.get('data_devolucao')

        if livro and livro.quantidade_disponivel < 1:
            raise ValidationError(f"O livro '{livro}' não está disponível.")

        if data_emprestimo and data_devolucao:
            if data_devolucao < data_emprestimo:
                raise ValidationError("A data de devolução não pode ser antes da data do empréstimo.")

        return cleaned_data