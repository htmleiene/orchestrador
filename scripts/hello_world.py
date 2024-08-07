import datetime
import logging

def main(user=None):
    # Configurando o logger
    logger = logging.getLogger(__name__)
    
    # Capturando o tempo atual
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Mensagem a ser exibida
    message = f"Hello, World! Current time is {current_time}"
    
    # Logando a mensagem
    logger.info(message)
    
    # Exibindo a mensagem (ou outro comportamento que queira testar)
    print(message)

    if user:
        print(f"Automação executada pelo usuário: {user}")
        logger.info(f"Automação executada pelo usuário: {user}")
