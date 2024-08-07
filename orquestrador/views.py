from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Automacao
from django.conf import settings
from .forms import AutomacaoForm
from .schedule import agendar_tarefa, executar_script
from .tasks import executar_script_task

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def logs(request):
    return render(request, 'logs.html')

@login_required
def debug(request):
    automacoes = Automacao.objects.all()
    return render(request, 'debug.html', {'automacoes': automacoes})

def robots(request):
    automacoes = Automacao.objects.all()  # Certifique-se de que as automações estão sendo recuperadas
    return render(request, 'robots.html', {'automacoes': automacoes})


@login_required
def add_automation(request):
    if request.method == 'POST':
        form = AutomacaoForm(request.POST, request.FILES)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            script = form.cleaned_data['script']  # Certifique-se de que o campo é capturado corretamente
            frequencia = form.cleaned_data['frequencia']
            horario_execucao = form.cleaned_data['horario_execucao']

            # Salvando o arquivo do script
            fs = FileSystemStorage(location=os.path.join(settings.SCRIPTS_ROOT))
            filename = fs.save(script.name, script)
            script_path = fs.url(filename)

            # Criação de nova automação
            nova_automacao = Automacao(nome=nome, script=filename, frequencia=frequencia, horario_execucao=horario_execucao)
            nova_automacao.save()

            # Verifique se a automação foi realmente salva
            print(f"Automação '{nova_automacao.nome}' salva com sucesso.")

            # Agendando a tarefa com os parâmetros corretos
            agendar_tarefa(nome, filename, frequencia, horario_execucao)

            return redirect('index')
        else:
            print("Formulário inválido:", form.errors)
            return render(request, 'add_automation.html', {'form': form})
    else:
        form = AutomacaoForm()
        return render(request, 'add_automation.html', {'form': form})


@login_required
def executar_automacao(request, automacao_id):
    automacao = Automacao.objects.get(id=automacao_id)
    try:
        # Usando Celery para executar o script em background
        resultado = executar_script.delay(automacao.script)
        automacao.status = 'Executado'
        automacao.save()
        return JsonResponse({'status': f'A automação {automacao.nome} está sendo executada em background.'})
    except Exception as e:
        logger.error(f'Erro ao executar a automação {automacao.nome}: {str(e)}')
        return JsonResponse({'mensagem': f'Erro ao executar a automação {automacao.nome}: {str(e)}'})

@login_required
def pausar_automacao(request, automacao_id):
    try:
        automacao = Automacao.objects.get(id=automacao_id)
        automacao.status = 'Pausado'
        automacao.save()
        return JsonResponse({'status': f'A automação {automacao.nome} foi pausada com sucesso!'})
    except Automacao.DoesNotExist:
        return JsonResponse({'error': 'Automação não encontrada'}, status=404)

@login_required
def retornar_automacao(request, automacao_id):
    try:
        automacao = Automacao.objects.get(id=automacao_id)
        automacao.status = 'Executando'
        automacao.save()
        return JsonResponse({'status': f'A automação {automacao.nome} foi retomada com sucesso!'})
    except Automacao.DoesNotExist:
        return JsonResponse({'error': 'Automação não encontrada'}, status=404)

@login_required
def remover_automacao(request, automacao_id):
    if request.method == 'DELETE':
        try:
            automacao = Automacao.objects.get(id=automacao_id)
            automacao.delete()
            return JsonResponse({'status': f'A automação {automacao.nome} foi removida com sucesso!'})
        except Automacao.DoesNotExist:
            return JsonResponse({'error': 'Automação não encontrada'}, status=404)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
def robots_data(request):
    automacoes = Automacao.objects.all()
    data = {
        automacao.id: {
            'nome': automacao.nome,
            'script': automacao.script,
            'horario': automacao.horario_execucao.strftime('%H:%M') if automacao.horario_execucao else 'Não especificado',
            'status': automacao.status,
        }
        for automacao in automacoes
    }
    return JsonResponse(data)

@login_required
def executar_debug(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        # Lógica de depuração simulada ou real pode ser inserida aqui
        data = {'status': f'A automação {nome} foi depurada com sucesso!'}
        return JsonResponse(data)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
def logs_debug(request):
    logs = "Log de depuração gerado..."
    return JsonResponse({'logs': logs})
