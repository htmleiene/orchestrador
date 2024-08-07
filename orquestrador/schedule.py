from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import importlib.util
import os
from django.conf import settings
from .models import Automacao

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()
scheduler.start()

def agendar_tarefa(nome_tarefa, script, frequencia, horario_execucao, user=None):
    try:
        if frequencia == 'diario':
            trigger = CronTrigger(day='*', hour=horario_execucao.hour, minute=horario_execucao.minute)
        elif frequencia == 'semanal':
            trigger = CronTrigger(week='*', day_of_week='mon', hour=horario_execucao.hour, minute=horario_execucao.minute) # ajuste conforme necessário
        elif frequencia == 'horario':
            trigger = CronTrigger(hour='*', minute=horario_execucao.minute)
        else:
            trigger = CronTrigger(day='*', hour='0', minute='0')

        scheduler.add_job(executar_script, trigger, id=nome_tarefa, kwargs={'script_name': script, 'user': user}, replace_existing=True)
        logger.info(f"Tarefa {nome_tarefa} agendada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao agendar a tarefa {nome_tarefa}: {e}")

def executar_script(script_name, user=None):
    try:
        script_path = os.path.join(settings.SCRIPTS_ROOT, script_name)
        spec = importlib.util.spec_from_file_location("module.name", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'main'):
            if user:
                module.main(user=user)
            else:
                module.main()
            logger.info(f"Script {script_name} executado com sucesso.")
        else:
            logger.error(f"Script {script_name} não possui uma função 'main'.")
    except Exception as e:
        logger.error(f"Erro ao executar o script {script_name}: {e}")
