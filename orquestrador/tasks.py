from celery import shared_task
import importlib.util
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def executar_script_task(script_name, user=None):
    try:
        logger.info(f"Executando script {script_name} com user: {user} (Tipo: {type(user)})")

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
