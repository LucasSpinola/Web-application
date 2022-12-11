from django import forms
from .models import Carro

class CadastroCarro(forms.ModelForm):
    class Meta:
        model = Carro
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.HiddenInput()
        

class CategoriaCarro(forms.Form):
    nome = forms.CharField(max_length=30)
    descricao = forms.CharField(max_length=60)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].widget = forms.Textarea()

