from django import forms
from store.models import Order


class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(
        label='Selecciona un archivo CSV',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    column = forms.CharField(
        label="Nombre de columna que contiene Order ID",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    status = forms.ChoiceField(
        label="Estado",
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
