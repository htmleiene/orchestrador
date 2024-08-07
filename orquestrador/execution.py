# orquestrador/execution.py
import importlib.util
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def executar_script(script_name, user=None):
    try:
        logger.info(f"Executando script {script_name} com user: {user} (Tipo: {type(user)})")

        if isinstance(user, str):
            logger.error(f"O valor de 'user' é uma string em vez de um objeto esperado: {user}")
            return {'mensagem': f"Erro: 'user' é uma string, mas deveria ser um objeto com atributos."}

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
            return {'mensagem': f"Script {script_name} não possui uma função 'main'."}
    except Exception as e:
        logger.error(f"Erro ao executar o script {script_name}: {e}")
        return {'mensagem': f"Erro ao executar o script {script_name}: {str(e)}"}

    return {'mensagem': f"Script {script_name} executado com sucesso."}
