from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o módulo de configurações do Django para o aplicativo Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetorpa.settings')

app = Celery('projetorpa')

# Configurações Celery devem usar o namespace 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobrir automaticamente as tasks nos pacotes 'tasks.py'
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
