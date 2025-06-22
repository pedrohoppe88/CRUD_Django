from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Perfil
from django.contrib.auth.decorators import login_required

def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        senha = request.POST['password']
        bio = request.POST.get('bio', '')
        nascimento = request.POST.get('nascimento', None)
        foto = request.FILES.get('foto', None)

        if User.objects.filter(username=username).exists():
            return render(request, 'usuarios/cadastro.html', {'erro': 'Usuário já existe'})

        # Cria o usuário
        user = User.objects.create_user(username=username, password=senha, email=email,
                                        first_name=first_name, last_name=last_name)
        # Cria o perfil
        perfil = Perfil(user=user, bio=bio)
        if nascimento:
            perfil.nascimento = nascimento
        if foto:
            perfil.foto = foto
        perfil.save()

        return redirect('login')

    return render(request, 'usuarios/cadastro.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['password']
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect('painel')
        else:
            return render(request, 'usuarios/login.html', {'erro': 'Usuário ou senha inválidos'})
    return render(request, 'usuarios/login.html')

def painel_view(request):
    return render(request, 'usuarios/painel.html')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')


@login_required
def painel_view(request):
    return render(request, 'usuarios/painel.html')