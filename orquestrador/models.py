from django.db import models

class Automacao(models.Model):
    FREQUENCIA_CHOICES = [
        ('Diário', 'Diário'),
        ('Semanal', 'Semanal'),
        ('Única Vez', 'Única Vez'),
    ]
    
    nome = models.CharField(max_length=255)
    script = models.TextField()
    frequencia = models.CharField(max_length=50, choices=FREQUENCIA_CHOICES)
    horario_execucao = models.TimeField(default="00:00:00")
    status = models.CharField(max_length=20, default='Agendado')

    def __str__(self):
        return self.nome
