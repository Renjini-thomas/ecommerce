from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model=Products
        fields='__all__'
        widgets = {
        'name' : forms.TextInput(attrs={'class':'form_control','placeholder':'name of the product'}),
        'price' : forms.NumberInput(attrs={'class':'form_control','placeholder':'price of the product'}),
        'desc' : forms.Textarea(attrs={'class':'form_control','placeholder':'description'}),
        }