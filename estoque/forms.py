from django import forms
from .models import Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nome', 'categoria', 'unidade_medida', 'quantidade_atual', 'quantidade_minima', 'data_validade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'unidade_medida': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_atual': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantidade_minima': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_validade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }