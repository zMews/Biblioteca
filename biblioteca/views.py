from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Aluno
from .forms import AlunoForm
from .models import Livro
from .forms import LivroForm
from .models import Emprestimo
from .forms import EmprestimoForm
from django.utils import timezone
from django.db.models import Q

def home(request):
    return render(request, 'biblioteca/base.html')

# Alunos

def aluno_list(request):
    alunos = Aluno.objects.all()
    return render(request, 'biblioteca/aluno_list.html', {'alunos': alunos})

def aluno_create(request):
    form = AlunoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('aluno_list')
    return render(request, 'biblioteca/aluno_form.html', {'form': form})

def aluno_update(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    form = AlunoForm(request.POST or None, instance=aluno)
    if form.is_valid():
        form.save()
        return redirect('aluno_list')
    return render(request, 'biblioteca/aluno_form.html', {'form': form})

def aluno_delete(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        aluno.delete()
        return redirect('aluno_list')
    return render(request, 'biblioteca/aluno_confirm_delete.html', {'aluno': aluno})

# Livros


def livro_list(request):
    livros = Livro.objects.all()
    return render(request, 'biblioteca/livro_list.html', {'livros': livros})

def livro_create(request):
    form = LivroForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('livro_list')
    return render(request, 'biblioteca/livro_form.html', {'form': form})

def livro_update(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    form = LivroForm(request.POST or None, instance=livro)
    if form.is_valid():
        form.save()
        return redirect('livro_list')
    return render(request, 'biblioteca/livro_form.html', {'form': form})

def livro_delete(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        return redirect('livro_list')
    return render(request, 'biblioteca/livro_confirm_delete.html', {'livro': livro})

# Emprestimo

def emprestimo_list(request):
    emprestimos_ativos = Emprestimo.objects.filter(data_devolvido__isnull=True)
    emprestimos_finalizados = Emprestimo.objects.filter(data_devolvido__isnull=False)

    return render(request, 'biblioteca/emprestimo_list.html', {
        'emprestimos_ativos': emprestimos_ativos,
        'emprestimos_finalizados': emprestimos_finalizados,
    })

def emprestimo_create(request):
    form = EmprestimoForm(request.POST or None)
    if form.is_valid():
        emprestimo = form.save(commit=False)
        emprestimo.save()
        # reduzir quantidade do livro
        livro = emprestimo.livro
        livro.quantidade_disponivel -= 1
        livro.save()
        return redirect('emprestimo_list')
    return render(request, 'biblioteca/emprestimo_form.html', {'form': form})

def emprestimo_devolver(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)

    if request.method == 'POST':
        if not emprestimo.data_devolvido:
            emprestimo.data_devolvido = timezone.now().date()
            emprestimo.save()

            # devolve 1 exemplar ao livro
            if emprestimo.livro:
                emprestimo.livro.quantidade_disponivel += 1
                emprestimo.livro.save()

        return redirect('emprestimo_list')

    return render(request, 'biblioteca/emprestimo_devolver.html', {'emprestimo': emprestimo})

def busca(request):
    termo = request.GET.get('q', '')

    alunos = Aluno.objects.filter(
        Q(nome__icontains=termo) |
        Q(matricula__icontains=termo)
    ) if termo else []

    livros = Livro.objects.filter(
        Q(titulo__icontains=termo) |
        Q(autor__icontains=termo) |
        Q(isbn__icontains=termo)
    ) if termo else []

    return render(request, 'biblioteca/busca.html', {
        'termo': termo,
        'alunos': alunos,
        'livros': livros,
    })
