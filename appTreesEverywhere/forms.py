from django import forms
from .models import PlantedTree, Account, Tree
from decimal import Decimal

class PlantedTreeForm(forms.ModelForm):
    """
    Formulário para adicionar uma nova árvore plantada.
    """
    latitude = forms.DecimalField(max_digits=10, decimal_places=6, required=True, label="Latitude")
    longitude = forms.DecimalField(max_digits=10, decimal_places=6, required=True, label="Longitude")
    account = forms.ModelChoiceField(queryset=Account.objects.all(), required=True, label="Account")
    tree = forms.ModelChoiceField(queryset=Tree.objects.all(), required=True, label="Árvore")
    age = forms.IntegerField(required=True, label="Idade")
    
    class Meta:
        model = PlantedTree
        fields = ['tree', 'latitude', 'longitude', 'account', 'age'] 

    def __init__(self, *args, **kwargs):
        # Recebe o parâmetro 'user' e o adiciona ao formulário
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Sobrescreve o método de save para associar corretamente a árvore ao usuário.
        """
        instance = super().save(commit=False)
        
        if self.user:
            instance.user = self.user  # Associa o usuário logado à árvore

        # Atribui as coordenadas como uma string (latitude, longitude)
        location = f"{self.cleaned_data['latitude']}, {self.cleaned_data['longitude']}"
        instance.location = location

        if commit:
            instance.save()
        return instance
