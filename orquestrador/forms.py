from django import forms
from .models import Automacao

class AutomacaoForm(forms.ModelForm):
    class Meta:
        model = Automacao
        fields = ['nome', 'script', 'frequencia', 'horario_execucao']
        widgets = {
            'frequencia': forms.Select(choices=[('Diário', 'Diário'), ('Semanal', 'Semanal')]),
        }

    script = forms.FileField(required=True)
